from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import GetPromptResult, Prompt, PromptArgument, PromptMessage, TextContent, Tool

from clickadvisor.cli.output import format_report_markdown
from clickadvisor.core.models import QueryContext
from clickadvisor.core.pipeline import AnalysisPipeline
from clickadvisor.core.version import detect_version
from clickadvisor.rules.registry import get_applicable_rules

server = Server("clickadvisor")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_query",
            description=(
                "Анализирует ClickHouse SQL-запрос на антипаттерны и проблемы производительности. "
                "Возвращает структурированный отчёт с формально обоснованными рекомендациями. "
                "Использует библиотеку из 20+ правил из реляционной алгебры и инвариантов ClickHouse. "
                "Не отправляет данные во внешние сервисы — работает локально. "
                "ВАЖНО: если пользователь упомянул версию ClickHouse в разговоре — "
                "всегда передавай её в ch_version. Если упомянул адрес кластера — "
                "сначала вызови detect_ch_version, потом analyze_query с полученной версией."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SQL запрос для анализа",
                    },
                    "ch_version": {
                        "type": "string",
                        "description": (
                            "Версия ClickHouse (например '25.3'). Если не указана — "
                            "применяются все правила."
                        ),
                        "default": None,
                    },
                    "schema_ddl": {
                        "type": "string",
                        "description": (
                            "DDL схемы таблиц (CREATE TABLE ...). Опционально, улучшает точность."
                        ),
                        "default": None,
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["diagnose", "explain"],
                        "description": (
                            "diagnose — краткий отчёт, explain — с объяснением принципов CH"
                        ),
                        "default": "diagnose",
                    },
                },
                "required": ["sql"],
            },
        ),
        Tool(
            name="analyze_query_json",
            description=(
                "То же что analyze_query, но возвращает структурированный JSON. "
                "Используй когда нужно программно обработать результаты."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "ch_version": {"type": "string", "default": None},
                    "schema_ddl": {"type": "string", "default": None},
                },
                "required": ["sql"],
            },
        ),
        Tool(
            name="list_rules",
            description="Возвращает список всех доступных правил оптимизации с описанием.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["1A", "1B", "1C", "detector", "all"],
                        "description": "Фильтр по типу правил",
                        "default": "all",
                    }
                },
            },
        ),
        Tool(
            name="detect_ch_version",
            description=(
                "Определяет версию ClickHouse подключаясь к кластеру через HTTP API. "
                "Используй этот инструмент первым если пользователь упомянул "
                "connection string или адрес кластера. Результат передай в ch_version "
                "при вызове analyze_query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "connect_url": {
                        "type": "string",
                        "description": "URL ClickHouse HTTP API, например http://localhost:8123",
                    },
                    "user": {"type": "string", "default": "default"},
                    "password": {"type": "string", "default": ""},
                },
                "required": ["connect_url"],
            },
        ),
    ]


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="analyze",
            description="Анализировать ClickHouse SQL запрос через ClickAdvisor",
            arguments=[
                PromptArgument(
                    name="sql",
                    description="SQL запрос для анализа",
                    required=True,
                ),
                PromptArgument(
                    name="ch_version",
                    description="Версия ClickHouse (например 25.3)",
                    required=False,
                ),
                PromptArgument(
                    name="mode",
                    description="diagnose или explain",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="explain",
            description="Объяснить почему ClickHouse запрос медленный",
            arguments=[
                PromptArgument(name="sql", required=True),
                PromptArgument(name="ch_version", required=False),
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, Any]) -> GetPromptResult:
    sql = str(arguments.get("sql", ""))
    ch_version = str(arguments.get("ch_version", ""))
    mode = str(arguments.get("mode", "diagnose"))
    version_hint = f" (ClickHouse {ch_version})" if ch_version else ""

    if name == "analyze":
        text = (
            f"Проанализируй этот ClickHouse SQL запрос{version_hint} "
            f"с помощью инструмента analyze_query и объясни что можно улучшить:\n\n"
            f"```sql\n{sql}\n```"
        )
        if ch_version:
            text += f"\n\nИспользуй ch_version='{ch_version}'"
        if mode == "explain":
            text += "\n\nИспользуй mode='explain' для подробных объяснений."
    elif name == "explain":
        text = (
            f"Объясни почему этот ClickHouse запрос{version_hint} работает медленно. "
            f"Используй инструмент analyze_query с mode='explain':\n\n"
            f"```sql\n{sql}\n```"
        )
    else:
        text = sql

    return GetPromptResult(
        description=f"ClickAdvisor: {name}",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=text),
            )
        ],
    )


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "analyze_query":
        return await _analyze_query(arguments)
    if name == "analyze_query_json":
        return await _analyze_query_json(arguments)
    if name == "list_rules":
        return await _list_rules(arguments)
    if name == "detect_ch_version":
        return await _detect_ch_version(arguments)
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _analyze_query(arguments: dict[str, Any]) -> list[TextContent]:
    sql = str(arguments["sql"])
    ch_version = arguments.get("ch_version")
    schema_ddl = arguments.get("schema_ddl")
    mode = str(arguments.get("mode", "diagnose"))
    if mode not in {"diagnose", "explain"}:
        mode = "diagnose"

    context = QueryContext(
        sql=sql,
        schema_ddl=str(schema_ddl) if schema_ddl is not None else None,
        ch_version=str(ch_version) if ch_version is not None else None,
    )

    rules = get_applicable_rules(context.ch_version)
    retrieval_advisor = _build_retrieval_advisor()
    pipeline = AnalysisPipeline(
        rules=rules,
        mode=mode,
        retrieval_advisor=retrieval_advisor,
    )
    report = pipeline.run(context)
    output = format_report_markdown(report, mode=mode)
    return [TextContent(type="text", text=output)]


async def _analyze_query_json(arguments: dict[str, Any]) -> list[TextContent]:
    sql = str(arguments["sql"])
    ch_version = arguments.get("ch_version")
    schema_ddl = arguments.get("schema_ddl")

    context = QueryContext(
        sql=sql,
        schema_ddl=str(schema_ddl) if schema_ddl is not None else None,
        ch_version=str(ch_version) if ch_version is not None else None,
    )
    rules = get_applicable_rules(context.ch_version)
    pipeline = AnalysisPipeline(rules=rules)
    report = pipeline.run(context)

    result = {
        "ch_version": report.query_context.ch_version or "unknown",
        "findings_count": len([finding for finding in report.findings if finding.tier != "rag"]),
        "findings": [
            {
                "rule_id": finding.rule_id,
                "tier": finding.tier,
                "severity": finding.severity,
                "description": finding.description,
                "suggestion": finding.suggestion,
                "example_before": finding.example_before,
                "example_after": finding.example_after,
                "confidence": finding.confidence,
            }
            for finding in report.findings
            if finding.tier != "rag"
        ],
        "rules_skipped_version": report.rules_skipped_version,
    }

    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def _list_rules(arguments: dict[str, Any]) -> list[TextContent]:
    tier_filter = str(arguments.get("tier", "all"))
    rules = get_applicable_rules(None)

    lines = ["# Правила оптимизации ClickAdvisor\n"]
    tier_order = {"1A": 0, "1B": 1, "1C": 2, "detector": 3, "rag": 4}
    sorted_rules = sorted(rules, key=lambda rule: (tier_order.get(rule.tier, 5), rule.rule_id))

    current_tier = None
    for rule in sorted_rules:
        if tier_filter != "all" and rule.tier != tier_filter:
            continue
        if rule.tier != current_tier:
            current_tier = rule.tier
            tier_labels = {
                "1A": "## Tier 1A — Формально эквивалентные (применяются автоматически)",
                "1B": "## Tier 1B — Приближённые (требуют opt-in)",
                "1C": "## Tier 1C — Условные (зависят от схемы или контекста)",
                "detector": "## Детекторы — Антипаттерны",
            }
            lines.append(tier_labels.get(current_tier, f"## {current_tier}"))
        lines.append(
            f"- **{rule.rule_id}** `{rule.name}` — доступно с CH {rule.ch_version_introduced}"
        )

    return [TextContent(type="text", text="\n".join(lines))]


async def _detect_ch_version(arguments: dict[str, Any]) -> list[TextContent]:
    connect_url = str(arguments["connect_url"])
    user = str(arguments.get("user", "default"))
    password = str(arguments.get("password", ""))

    version = detect_version(connect_url, user=user, password=password)
    if version:
        return [
            TextContent(
                type="text",
                text=(
                    f"ClickHouse version: {version}\n\n"
                    f"Используй ch_version='{version}' при вызове analyze_query "
                    f"для версионированных рекомендаций."
                ),
            )
        ]

    return [
        TextContent(
            type="text",
            text=(
                f"Не удалось подключиться к {connect_url}. "
                f"Проверьте URL, user и password. "
                f"Можно продолжить анализ без версии — будут применены все правила."
            ),
        )
    ]


def _build_retrieval_advisor() -> Any | None:
    try:
        from clickadvisor.retrieval.advisory import RetrievalAdvisor

        if Path(".qdrant_db").exists():
            return RetrievalAdvisor()
    except Exception:
        return None
    return None


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run() -> None:
    asyncio.run(main())
