from __future__ import annotations

import argparse
import hashlib
import logging
import os
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import requests
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

try:
    import xmltodict
except ModuleNotFoundError:
    xmltodict = None

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
BACKOFF_BASE_SECONDS = 2.0
USER_AGENT = "ClickAdvisorKB/0.1 (+https://github.com/openai/codex)"
BLOG_MIN_EXPECTED_POSTS = 150


@dataclass(slots=True)
class SourceConfig:
    name: str
    kind: str
    output_subdir: str
    sitemap_url: str | None = None
    rss_url: str | None = None
    allowed_prefixes: list[str] | None = None
    allowed_url_prefixes: list[str] | None = None
    excluded_urls: list[str] | None = None
    excluded_url_prefixes: list[str] | None = None
    start_urls: list[str] | None = None
    allowed_domains: list[str] | None = None
    api_url: str | None = None
    limit: int | None = None


def load_sources(config_path: Path) -> list[SourceConfig]:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return [SourceConfig(**source) for source in raw["sources"]]


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        session.headers.update({"Authorization": f"Bearer {github_token}"})
    return session


def fetch_with_retry(
    session: requests.Session,
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    params: dict[str, Any] | None = None,
) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=timeout, params=params)
            response.raise_for_status()
            return response
        except Exception as exc:
            last_error = exc
            if attempt == retries - 1:
                break
            time.sleep(BACKOFF_BASE_SECONDS**attempt)
    assert last_error is not None
    raise last_error


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def url_allowed(url: str, source: SourceConfig) -> bool:
    parsed = urlparse(url)
    if source.allowed_domains and parsed.netloc not in source.allowed_domains:
        return False
    if source.allowed_url_prefixes and not any(
        url.startswith(prefix) for prefix in source.allowed_url_prefixes
    ):
        return False
    if source.excluded_urls and url in source.excluded_urls:
        return False
    if source.excluded_url_prefixes and any(
        url.startswith(prefix) for prefix in source.excluded_url_prefixes
    ):
        return False
    path = parsed.path or "/"
    if source.allowed_prefixes:
        return any(path.startswith(prefix) for prefix in source.allowed_prefixes)
    return True


def slugify_url(url: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    safe_path = path.replace("/", "__")
    return f"{safe_path}--{digest}"


def extract_main_html(html: str, url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.find("article") or soup.body or soup
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    return f"<h1>{title}</h1>\n{str(main)}"


def convert_html_to_markdown(html: str) -> str:
    return (
        html_to_markdown(
            html,
            heading_style="ATX",
            bullets="-",
            strip=["script", "style"],
        ).strip()
        + "\n"
    )


def parse_xml_document(xml_text: str) -> dict[str, Any]:
    if xmltodict is not None:
        return xmltodict.parse(xml_text)

    root = ElementTree.fromstring(xml_text)
    local_name = root.tag.split("}", 1)[-1]

    if local_name == "urlset":
        urls = []
        for child in root:
            child_name = child.tag.split("}", 1)[-1]
            if child_name != "url":
                continue
            item: dict[str, Any] = {}
            for field in child:
                field_name = field.tag.split("}", 1)[-1]
                item[field_name] = (field.text or "").strip()
            urls.append(item)
        return {"urlset": {"url": urls}}

    if local_name == "sitemapindex":
        sitemaps = []
        for child in root:
            child_name = child.tag.split("}", 1)[-1]
            if child_name != "sitemap":
                continue
            item: dict[str, Any] = {}
            for field in child:
                field_name = field.tag.split("}", 1)[-1]
                item[field_name] = (field.text or "").strip()
            sitemaps.append(item)
        return {"sitemapindex": {"sitemap": sitemaps}}

    if local_name == "rss":
        channel_node = None
        for child in root:
            if child.tag.split("}", 1)[-1] == "channel":
                channel_node = child
                break
        items: list[dict[str, str]] = []
        if channel_node is not None:
            for child in channel_node:
                if child.tag.split("}", 1)[-1] != "item":
                    continue
                item: dict[str, str] = {}
                for field in child:
                    field_name = field.tag.split("}", 1)[-1]
                    item[field_name] = (field.text or "").strip()
                items.append(item)
        return {"rss": {"channel": {"item": items}}}

    raise ValueError(f"Unsupported XML root: {local_name}")


def normalize_source_selector(selector: str) -> str:
    selector = selector.strip()
    aliases = {
        "blog": "clickhouse.com/blog",
        "releases": "github.com/ClickHouse/ClickHouse/releases",
    }
    return aliases.get(selector, selector)


def discover_from_sitemap_url(session: requests.Session, sitemap_url: str) -> list[str]:
    xml_text = fetch_with_retry(session, sitemap_url).text
    document = parse_xml_document(xml_text)

    urls: list[str] = []
    sitemap_index = document.get("sitemapindex")
    if sitemap_index:
        for sitemap in ensure_list(sitemap_index.get("sitemap")):
            loc = sitemap.get("loc")
            if isinstance(loc, str):
                urls.extend(discover_from_sitemap_url(session, loc.strip()))
        return urls

    urlset = document.get("urlset")
    if urlset:
        for item in ensure_list(urlset.get("url")):
            loc = item.get("loc")
            if isinstance(loc, str):
                urls.append("".join(loc.split()))
    return urls


def discover_from_rss(session: requests.Session, rss_url: str) -> list[str]:
    xml_text = fetch_with_retry(session, rss_url).text
    document = parse_xml_document(xml_text)
    channel = document.get("rss", {}).get("channel", {})
    urls: list[str] = []
    for item in ensure_list(channel.get("item")):
        link = item.get("link")
        if isinstance(link, str):
            urls.append(link.strip())
    return urls


def discover_from_sitemap(session: requests.Session, source: SourceConfig) -> list[str]:
    assert source.sitemap_url is not None
    try:
        sitemap_urls = discover_from_sitemap_url(session, source.sitemap_url)
    except Exception as exc:
        logging.warning("Sitemap discovery failed for %s: %s", source.name, exc)
        sitemap_urls = []

    filtered = sorted({url for url in sitemap_urls if url_allowed(url, source)})
    if filtered:
        return filtered

    if source.rss_url:
        logging.warning(
            "Sitemap for %s unavailable or empty after filtering; falling back to RSS",
            source.name,
        )
        rss_urls = discover_from_rss(session, source.rss_url)
        return sorted({url for url in rss_urls if url_allowed(url, source)})
    return []


def discover_domain_pages(session: requests.Session, source: SourceConfig) -> list[str]:
    assert source.start_urls is not None
    visited: set[str] = set()
    queue = list(source.start_urls)
    discovered: list[str] = []
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            html = fetch_with_retry(session, url).text
        except Exception:
            continue
        discovered.append(url)
        soup = BeautifulSoup(html, "html.parser")
        for anchor in soup.select("a[href]"):
            candidate = urljoin(url, anchor["href"])
            if candidate in visited or not url_allowed(candidate, source):
                continue
            queue.append(candidate)
    return discovered


def discover_github_releases(session: requests.Session, source: SourceConfig) -> list[dict[str, Any]]:
    assert source.api_url is not None
    limit = source.limit or 36
    releases = fetch_with_retry(
        session,
        source.api_url,
        params={"per_page": min(limit, 100), "page": 1},
    ).json()
    return list(releases[:limit])


def write_html_and_markdown_outputs(
    output_dir: Path,
    source_name: str,
    url: str,
    raw_html: str,
    markdown: str,
) -> None:
    slug = slugify_url(url)
    raw_dir = output_dir / "raw" / source_name
    md_dir = output_dir / "markdown" / source_name
    raw_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / f"{slug}.html").write_text(raw_html, encoding="utf-8")
    (md_dir / f"{slug}.md").write_text(markdown, encoding="utf-8")


def release_markdown(item: dict[str, Any]) -> str:
    tag_name = str(item.get("tag_name", "")).strip()
    release_date = str(item.get("published_at", "")).strip()
    is_lts = "-lts" in tag_name.lower()
    frontmatter = {
        "version": tag_name,
        "release_date": release_date,
        "is_lts": is_lts,
        "url": item.get("html_url", ""),
        "tag_name": tag_name,
    }
    body = (item.get("body") or "").strip()
    return "---\n" + yaml.safe_dump(frontmatter, sort_keys=False).strip() + "\n---\n\n" + body + "\n"


def write_release_outputs(output_dir: Path, source_name: str, item: dict[str, Any]) -> None:
    url = str(item["html_url"])
    slug = slugify_url(url)
    markdown = release_markdown(item)
    raw_dir = output_dir / "raw" / source_name
    md_dir = output_dir / "markdown" / source_name
    raw_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / f"{slug}.md").write_text(markdown, encoding="utf-8")
    (md_dir / f"{slug}.md").write_text(markdown, encoding="utf-8")


def crawl_source(
    session: requests.Session,
    source: SourceConfig,
    output_dir: Path,
    skipped_log_path: Path,
) -> int:
    if source.kind == "sitemap":
        items: Iterable[str | dict[str, Any]] = discover_from_sitemap(session, source)
    elif source.kind == "domain":
        items = discover_domain_pages(session, source)
    elif source.kind == "github_releases":
        items = discover_github_releases(session, source)
    else:
        raise ValueError(f"Unsupported source kind: {source.kind}")

    item_list = list(items)
    if source.name == "clickhouse.com/blog" and len(item_list) < BLOG_MIN_EXPECTED_POSTS:
        logging.warning(
            "Blog discovery returned only %s URLs; expected at least %s. Inspect sitemap/RSS filters.",
            len(item_list),
            BLOG_MIN_EXPECTED_POSTS,
        )

    crawled = 0
    for item in item_list:
        try:
            if isinstance(item, dict):
                write_release_outputs(output_dir, source.output_subdir, item)
            else:
                response = fetch_with_retry(session, item)
                raw_html = extract_main_html(response.text, item)
                markdown = convert_html_to_markdown(raw_html)
                write_html_and_markdown_outputs(
                    output_dir,
                    source.output_subdir,
                    item,
                    raw_html,
                    markdown,
                )
            crawled += 1
        except Exception as exc:
            skipped_log_path.parent.mkdir(parents=True, exist_ok=True)
            with skipped_log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"{source.name}\t{item}\t{exc}\n")
    return crawled


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl documentation sources for the KB.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("scripts/kb/sources.yaml"),
        help="Path to the YAML source configuration.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/kb"),
        help="Directory for raw and markdown artifacts.",
    )
    parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        default=[],
        help="Optional source name filter. Can be repeated.",
    )
    parser.add_argument(
        "--only",
        action="append",
        dest="sources",
        help="Alias for --source. Supports short names like 'blog' and 'releases'.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Accepted for compatibility. Current crawler always overwrites matching outputs in place.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    session = make_session()
    skipped_log_path = args.output_dir / "logs" / "skipped_urls.log"
    sources = load_sources(args.config)
    selected_names = {normalize_source_selector(name) for name in args.sources}
    selected_sources = [s for s in sources if not selected_names or s.name in selected_names]
    for source in selected_sources:
        count = crawl_source(session, source, args.output_dir, skipped_log_path)
        logging.info("Crawled %s documents from %s", count, source.name)


if __name__ == "__main__":
    main()
