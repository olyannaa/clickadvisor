from __future__ import annotations

import json

import pytest

from clickadvisor.mcp_server import server as mcp_server
from clickadvisor.mcp_server.server import call_tool


@pytest.mark.asyncio
async def test_analyze_query_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mcp_server, "_build_retrieval_advisor", lambda: None)

    results = await call_tool(
        "analyze_query",
        {
            "sql": "SELECT COUNT(DISTINCT user_id) FROM events",
            "ch_version": "25.3",
        },
    )
    assert len(results) == 1
    assert "R-001" in results[0].text
    assert "uniqExact" in results[0].text


@pytest.mark.asyncio
async def test_analyze_query_json() -> None:
    results = await call_tool(
        "analyze_query_json",
        {
            "sql": "SELECT COUNT(DISTINCT user_id) FROM events",
        },
    )
    data = json.loads(results[0].text)
    assert "findings" in data
    assert any(finding["rule_id"] == "R-001" for finding in data["findings"])


@pytest.mark.asyncio
async def test_list_rules() -> None:
    results = await call_tool("list_rules", {})
    assert "R-001" in results[0].text
    assert "Tier 1A" in results[0].text


@pytest.mark.asyncio
async def test_detect_ch_version_unreachable() -> None:
    results = await call_tool(
        "detect_ch_version",
        {
            "connect_url": "http://localhost:19999",
        },
    )
    assert "Не удалось подключиться" in results[0].text


@pytest.mark.asyncio
async def test_list_prompts() -> None:
    from clickadvisor.mcp_server.server import list_prompts

    prompts = await list_prompts()
    assert len(prompts) == 2
    names = [prompt.name for prompt in prompts]
    assert "analyze" in names
    assert "explain" in names


def test_build_fastmcp_server() -> None:
    from clickadvisor.mcp_server.server import build_fastmcp_server

    app = build_fastmcp_server(host="127.0.0.1", port=8765, path="/mcp")
    assert app is not None


@pytest.mark.asyncio
async def test_unknown_tool() -> None:
    results = await call_tool("unknown_tool", {})
    assert "Unknown tool" in results[0].text
