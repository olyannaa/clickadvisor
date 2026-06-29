from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml

REQUIRED_FIELDS = {
    "source",
    "url",
    "topic",
    "ch_version_introduced",
    "last_updated",
    "chunk_index",
    "total_chunks_in_doc",
}
WEB_SOURCES = {
    "blog",
    "clickhouse.com_blog",
    "docs.clickhouse.com",
    "github_releases",
    "kb.altinity.com",
    "releases",
}


@dataclass(slots=True)
class ValidationIssue:
    path: Path
    message: str


@dataclass(slots=True)
class ChunkDocument:
    path: Path
    frontmatter: dict[str, object]
    body: str
    content_hash: str
    links: list[str]


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter start delimiter")
    _, _, remainder = text.partition("---\n")
    frontmatter_text, delimiter, body = remainder.partition("\n---\n")
    if not delimiter:
        raise ValueError("missing YAML frontmatter end delimiter")
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    return frontmatter, body.strip()


def extract_links(markdown_body: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown_body)


def load_chunk_document(path: Path) -> ChunkDocument:
    frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"))
    normalized = re.sub(r"\s+", " ", body).strip()
    content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return ChunkDocument(
        path=path,
        frontmatter=frontmatter,
        body=body,
        content_hash=content_hash,
        links=extract_links(body),
    )


def validate_frontmatter(document: ChunkDocument) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    missing = REQUIRED_FIELDS - set(document.frontmatter.keys())
    if missing:
        issues.append(
            ValidationIssue(path=document.path, message=f"missing fields: {sorted(missing)}")
        )
    if not document.body:
        issues.append(ValidationIssue(path=document.path, message="empty chunk body"))
    return issues


def find_duplicate_hashes(documents: list[ChunkDocument]) -> list[ValidationIssue]:
    seen: dict[str, Path] = {}
    issues: list[ValidationIssue] = []
    for document in documents:
        digest = document.content_hash
        if digest in seen:
            issues.append(
                ValidationIssue(
                    path=document.path,
                    message=f"duplicate content hash with {seen[digest]}",
                )
            )
        else:
            seen[digest] = document.path
    return issues


def is_http_link(link: str) -> bool:
    return link.startswith("http://") or link.startswith("https://")


def document_base_url(document: ChunkDocument) -> str | None:
    base_url = document.frontmatter.get("url")
    if not isinstance(base_url, str) or not base_url:
        return None
    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        return None
    return base_url


def document_source(document: ChunkDocument) -> str:
    source = document.frontmatter.get("source")
    return source if isinstance(source, str) else ""


def is_potential_web_relative_link(link: str, document: ChunkDocument) -> bool:
    if link.startswith("#") or is_http_link(link):
        return False
    if urlparse(link).scheme:
        return False
    if document_source(document) in WEB_SOURCES:
        return True
    return document_base_url(document) is not None and (
        link.startswith("/")
        or link.startswith("./")
        or link.startswith("../")
        or "/" in link
    )


def document_relative_to_absolute(link: str, document: ChunkDocument) -> str | None:
    base_url = document_base_url(document)
    if base_url is None:
        return None
    if link.startswith("/"):
        parsed = urlparse(base_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        return urljoin(origin, link)
    if link.startswith("./") or link.startswith("../") or (
        not link.startswith("#") and not is_http_link(link) and not urlparse(link).scheme and "/" in link
    ) or (
        not link.startswith("#") and not is_http_link(link) and "." not in Path(link).name
    ):
        return urljoin(base_url, link)
    return None


def validate_link(
    link: str,
    document: ChunkDocument,
    external_link_cache: dict[str, str | None],
    session: requests.Session | None,
) -> str | None:
    if link.startswith("#"):
        return None
    absolute_http_link = document_relative_to_absolute(link, document)
    if absolute_http_link is not None:
        link = absolute_http_link
    if is_http_link(link):
        if link in external_link_cache:
            return external_link_cache[link]
        if session is None:
            return None
        try:
            response = session.head(link, allow_redirects=True, timeout=5)
            if response.status_code >= 400:
                response = session.get(link, timeout=10)
            if response.status_code >= 400:
                external_link_cache[link] = f"broken external link: {link}"
                return external_link_cache[link]
        except Exception as exc:
            external_link_cache[link] = f"broken external link: {link} ({exc})"
            return external_link_cache[link]
        external_link_cache[link] = None
        return None

    if is_potential_web_relative_link(link, document):
        return None

    absolute_path = (document.path.parent / link).resolve()
    parsed = urlparse(link)
    if parsed.scheme or parsed.netloc:
        return None
    if not absolute_path.exists():
        return f"broken local link: {link}"
    return None


def validate_links(
    document: ChunkDocument,
    *,
    check_external_links: bool,
    external_link_cache: dict[str, str | None],
    session: requests.Session | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    active_session = session if check_external_links else None
    for link in document.links:
        issue = validate_link(link, document, external_link_cache, active_session)
        if issue:
            issues.append(ValidationIssue(path=document.path, message=issue))
    return issues


def validate_chunk_tree(root: Path, *, check_external_links: bool = False) -> list[ValidationIssue]:
    chunk_paths = sorted(root.rglob("*.md"))
    issues: list[ValidationIssue] = []
    documents: list[ChunkDocument] = []

    for path in chunk_paths:
        try:
            document = load_chunk_document(path)
        except Exception as exc:
            issues.append(ValidationIssue(path=path, message=str(exc)))
            continue
        documents.append(document)
        issues.extend(validate_frontmatter(document))

    valid_documents = [
        document for document in documents if not any(issue.path == document.path for issue in issues)
    ]
    issues.extend(find_duplicate_hashes(valid_documents))

    external_link_cache: dict[str, str | None] = {}
    session = requests.Session() if check_external_links else None
    for document in valid_documents:
        issues.extend(
            validate_links(
                document,
                check_external_links=check_external_links,
                external_link_cache=external_link_cache,
                session=session,
            )
        )
    return issues


def deduplicate_chunk_tree(root: Path) -> tuple[int, int]:
    chunk_paths = sorted(root.rglob("*.md"))
    seen_hashes: dict[str, Path] = {}
    deleted_count = 0

    for path in chunk_paths:
        document = load_chunk_document(path)
        first_path = seen_hashes.get(document.content_hash)
        if first_path is None:
            seen_hashes[document.content_hash] = path
            continue
        path.unlink()
        deleted_count += 1

    remaining_count = len(list(root.rglob("*.md")))
    return deleted_count, remaining_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate chunked KB artifacts.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/kb/chunks"))
    parser.add_argument(
        "--check-external-links",
        action="store_true",
        help="Verify external HTTP/HTTPS links. Disabled by default for speed on large KBs.",
    )
    parser.add_argument(
        "--dedup",
        action="store_true",
        help="Delete duplicate chunk files by content hash, keeping the first path alphabetically.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.dedup:
        deleted_count, remaining_count = deduplicate_chunk_tree(args.input_dir)
        print(f"Deleted {deleted_count} duplicate files. {remaining_count} files remain.")
        return
    issues = validate_chunk_tree(args.input_dir, check_external_links=args.check_external_links)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}")
        raise SystemExit(1)
    print(f"Validated {len(list(args.input_dir.rglob('*.md')))} chunks without issues.")


if __name__ == "__main__":
    main()
