"""
Entry point for `python -m clickadvisor.mcp_server`.

Supports --transport stdio (default) and --transport sse for Docker/Railway.
"""

from __future__ import annotations

import argparse


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ClickAdvisor MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport to use (default: stdio)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (SSE mode)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (SSE mode)")
    return parser.parse_args()


def _run_sse(host: str, port: int) -> None:
    import uvicorn
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.routing import Mount, Route

    from clickadvisor.mcp_server.server import server

    sse_transport = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> Response:
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], server.create_initialization_options()
            )
        return Response()

    async def handle_health(request: Request) -> Response:
        return Response("ok", media_type="text/plain")

    starlette_app = Starlette(
        routes=[
            Route("/health", handle_health),
            Route("/sse", handle_sse),
            Mount("/messages/", app=sse_transport.handle_post_message),
        ]
    )

    uvicorn.run(starlette_app, host=host, port=port)


def main() -> None:
    args = _parse_args()

    if args.transport == "sse":
        _run_sse(args.host, args.port)
    else:
        from clickadvisor.mcp_server.server import run
        run()


if __name__ == "__main__":
    main()
