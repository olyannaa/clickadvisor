from __future__ import annotations

import json
from typing import Any

import pytest

from clickadvisor.mcp_server import server as mcp_server
from clickadvisor.mcp_server.server import HttpSecurityMiddleware, call_tool, run_http


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


def test_remote_http_requires_bearer_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CLICKADVISOR_MCP_BEARER_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="CLICKADVISOR_MCP_BEARER_TOKEN"):
        run_http(host="0.0.0.0", port=8765, path="/mcp")


@pytest.mark.asyncio
async def test_http_security_middleware_requires_bearer_token() -> None:
    async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})

    middleware = HttpSecurityMiddleware(app, bearer_token="secret", rate_limit_per_minute=10)
    sent: list[dict[str, Any]] = []

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await middleware(
        {"type": "http", "headers": [], "client": ("127.0.0.1", 12345)},
        lambda: None,
        send,
    )

    assert sent[0]["status"] == 401


@pytest.mark.asyncio
async def test_http_security_middleware_accepts_valid_bearer_token() -> None:
    async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})

    middleware = HttpSecurityMiddleware(app, bearer_token="secret", rate_limit_per_minute=10)
    sent: list[dict[str, Any]] = []

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await middleware(
        {
            "type": "http",
            "headers": [(b"authorization", b"Bearer secret")],
            "client": ("127.0.0.1", 12345),
        },
        lambda: None,
        send,
    )

    assert sent[0]["status"] == 200


@pytest.mark.asyncio
async def test_unknown_tool() -> None:
    results = await call_tool("unknown_tool", {})
    assert "Unknown tool" in results[0].text
