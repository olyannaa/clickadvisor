from __future__ import annotations

import argparse
import hashlib
import math
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

TOKEN_TARGET = 500
TOKEN_OVERLAP = 50
VERSION_PATTERN = re.compile(r"\b(?:v)?(\d{2}\.\d+|\d+\.\d+)\b")


@dataclass(slots=True)
class Chunk:
    content: str
    chunk_index: int
    total_chunks: int


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text.split()) * 1.3))


def split_markdown_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    in_code_block = False
    in_table = False

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
        is_table_line = "|" in line and stripped.count("|") >= 2
        if is_table_line:
            in_table = True
        elif in_table and stripped:
            in_table = False

        current.append(line)
        if not in_code_block and not in_table and not stripped:
            blocks.append("\n".join(current).strip("\n"))
            current = []

    if current:
        blocks.append("\n".join(current).strip("\n"))
    return [block for block in blocks if block.strip()]


def overlap_tail(text: str, target_tokens: int) -> str:
    words = text.split()
    if not words:
        return ""
    approx_words = max(1, round(target_tokens / 1.3))
    tail = words[-approx_words:]
    return " ".join(tail)


def build_chunks(markdown: str, token_target: int = TOKEN_TARGET, overlap: int = TOKEN_OVERLAP) -> list[str]:
    blocks = split_markdown_blocks(markdown)
    if not blocks:
        return []

    chunks: list[str] = []
    current = ""
    for block in blocks:
        candidate = block if not current else f"{current}\n\n{block}"
        if current and estimate_tokens(candidate) > token_target:
            chunks.append(current.strip())
            tail = overlap_tail(current, overlap)
            current = f"{tail}\n\n{block}".strip() if tail else block
        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())
    return chunks


def detect_version(markdown: str) -> str:
    match = VERSION_PATTERN.search(markdown)
    return match.group(1) if match else "auto"


def extract_topic(path: Path, markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return slugify(line[2:].strip())
    return slugify(path.stem)


def slugify(value: str) -> str:
    lowered = value.lower()
    return re.sub(r"[^a-z0-9]+", "-", lowered).strip("-") or "untitled"


def frontmatter_for_chunk(
    *,
    source: str,
    url: str,
    topic: str,
    version: str,
    last_updated: str,
    chunk_index: int,
    total_chunks: int,
) -> str:
    data = {
        "source": source,
        "url": url,
        "topic": topic,
        "ch_version_introduced": version,
        "last_updated": last_updated,
        "chunk_index": chunk_index,
        "total_chunks_in_doc": total_chunks,
    }
    return "---\n" + yaml.safe_dump(data, sort_keys=False).strip() + "\n---\n\n"


def source_from_path(path: Path, markdown_root: Path) -> str:
    relative = path.relative_to(markdown_root)
    return relative.parts[0]


def url_from_markdown(markdown: str) -> str:
    first_link = re.search(r"https?://\S+", markdown)
    return first_link.group(0).rstrip(").,") if first_link else "unknown"


def chunk_document(path: Path, markdown_root: Path, output_dir: Path) -> list[Path]:
    markdown = path.read_text(encoding="utf-8")
    chunks = build_chunks(markdown)
    source = source_from_path(path, markdown_root)
    topic = extract_topic(path, markdown)
    version = detect_version(markdown)
    url = url_from_markdown(markdown)
    last_updated = date.today().isoformat()
    output_source_dir = output_dir / source / slugify(path.stem)
    output_source_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    for index, chunk_content in enumerate(chunks, start=1):
        frontmatter = frontmatter_for_chunk(
            source=source,
            url=url,
            topic=topic,
            version=version,
            last_updated=last_updated,
            chunk_index=index,
            total_chunks=len(chunks),
        )
        chunk_text = frontmatter + chunk_content.strip() + "\n"
        chunk_hash = hashlib.sha1(chunk_text.encode("utf-8")).hexdigest()[:8]
        chunk_path = output_source_dir / f"{index:03d}-{chunk_hash}.md"
        chunk_path.write_text(chunk_text, encoding="utf-8")
        written_paths.append(chunk_path)
    return written_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chunk markdown KB documents.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/kb/markdown"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/kb/chunks"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for markdown_file in sorted(args.input_dir.rglob("*.md")):
        chunk_document(markdown_file, args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
