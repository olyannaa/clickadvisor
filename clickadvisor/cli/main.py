from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress

from clickadvisor import __version__
from clickadvisor.cli.output import (
    print_report_console,
    print_report_json,
    print_report_markdown,
)
from clickadvisor.core.models import QueryContext
from clickadvisor.core.pipeline import AnalysisPipeline
from clickadvisor.core.version import detect_version
from clickadvisor.rules.registry import get_all_rules

app = typer.Typer(
    help="Local-first CLI advisor for ClickHouse query optimization.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def _read_optional(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.read_text(encoding="utf-8")


def _read_environment(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise typer.BadParameter(f"invalid environment JSON: {error}") from error
    if not isinstance(payload, dict):
        raise typer.BadParameter("environment JSON must be an object")
    return payload


@app.command()
def version() -> None:
    console.print(f"ClickAdvisor {__version__}")


@app.command()
def mcp_server() -> None:
    """Запустить MCP сервер для интеграции с Claude Desktop и другими LLM."""
    from clickadvisor.mcp_server.server import run

    run()


@app.command()
def mcp_http_server(
    host: Annotated[str, typer.Option(help="Bind host")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port")] = 8765,
    path: Annotated[str, typer.Option(help="MCP endpoint path")] = "/mcp",
) -> None:
    """Запустить Streamable HTTP MCP сервер для remote-compatible demo."""
    from clickadvisor.mcp_server.server import run_http

    if host not in {"127.0.0.1", "localhost"}:
        console.print(
            "[yellow]Внимание: remote MCP endpoint должен быть защищён HTTPS/auth proxy. "
            "Для локального demo безопаснее использовать 127.0.0.1.[/yellow]"
        )
    run_http(host=host, port=port, path=path)


@app.command()
def analyze(
    sql: Annotated[Path, typer.Option(help="SQL файл")],
    explain: Annotated[Path | None, typer.Option()] = None,
    schema: Annotated[Path | None, typer.Option()] = None,
    environment: Annotated[Path | None, typer.Option(help="Environment JSON file")] = None,
    connect: Annotated[str | None, typer.Option(help="clickhouse://host:9000")] = None,
    ch_version: Annotated[str | None, typer.Option(help="24.3")] = None,
    ch_user: Annotated[str, typer.Option(help="ClickHouse user")] = "default",
    ch_password: Annotated[str, typer.Option(help="ClickHouse password")] = "",
    mode: Annotated[str, typer.Option(help="diagnose|explain")] = "diagnose",
    output_format: Annotated[
        str,
        typer.Option(help="console|json|markdown"),
    ] = "console",
    retrieval: Annotated[
        bool | None,
        typer.Option(
            "--retrieval/--no-retrieval",
            help="Включить retrieval advisory, если Qdrant KB доступна",
        ),
    ] = None,
    explain_estimate: Annotated[
        bool,
        typer.Option(
            "--explain-estimate/--no-explain-estimate",
            help="Запускать EXPLAIN ESTIMATE через ClickHouse HTTP API",
        ),
    ] = False,
) -> None:
    if mode not in {"diagnose", "explain"}:
        raise typer.BadParameter("mode must be one of: diagnose, explain")
    if output_format not in {"console", "json", "markdown"}:
        raise typer.BadParameter("output_format must be one of: console, json, markdown")

    sql_text = sql.read_text(encoding="utf-8")
    explain_text = _read_optional(explain)
    schema_text = _read_optional(schema)
    environment_data = _read_environment(environment)

    version = ch_version
    if connect and not ch_version:
        version = detect_version(connect, user=ch_user, password=ch_password)

    context = QueryContext(
        sql=sql_text,
        explain_output=explain_text,
        schema_ddl=schema_text,
        ch_version=version,
        environment=environment_data,
    )

    rules = get_all_rules()
    retrieval_advisor = None
    qdrant_db_path = Path(".qdrant_db")
    should_use_retrieval = qdrant_db_path.exists() if retrieval is None else retrieval
    if should_use_retrieval and qdrant_db_path.exists():
        from clickadvisor.retrieval.advisory import RetrievalAdvisor

        retrieval_advisor = RetrievalAdvisor(db_path=str(qdrant_db_path))
    elif retrieval:
        console.print(
            "[yellow]Retrieval advisory отключён: .qdrant_db не найден. "
            "Запустите `chadvisor index-kb`.[/yellow]"
        )

    explain_comparator = None
    if explain_estimate and connect:
        from clickadvisor.explain.comparator import ExplainComparator
        from clickadvisor.explain.estimator import ExplainEstimator

        estimator = ExplainEstimator(connect, user=ch_user, password=ch_password)
        explain_comparator = ExplainComparator(estimator)
    elif explain_estimate:
        console.print(
            "[yellow]EXPLAIN ESTIMATE отключён: требуется параметр --connect.[/yellow]"
        )

    pipeline = AnalysisPipeline(
        rules,
        mode=mode,
        retrieval_advisor=retrieval_advisor,
        explain_comparator=explain_comparator,
    )
    report = pipeline.run(context)

    if output_format == "console":
        print_report_console(report, mode=mode, console=console)
        return
    if output_format == "json":
        print_report_json(report, console=console)
        return
    if output_format == "markdown":
        print_report_markdown(report, mode=mode, console=console)
        return


@app.command()
def workload(
    query_log: Annotated[
        Path | None,
        typer.Option(help="Sanitized CSV export from system.query_log"),
    ] = None,
    connect: Annotated[
        str | None,
        typer.Option(help="ClickHouse HTTP URL for live mode, e.g. http://localhost:8123"),
    ] = None,
    since: Annotated[
        str,
        typer.Option(help="Live query_log window: 15m, 24h, 7d, 2w"),
    ] = "24h",
    ch_user: Annotated[str, typer.Option("--user", help="ClickHouse user (live mode)")] = "default",
    ch_password: Annotated[
        str, typer.Option("--password", help="ClickHouse password (live mode)")
    ] = "",
    top_n: Annotated[int, typer.Option(help="Number of normalized query groups to show")] = 10,
    ch_version: Annotated[str | None, typer.Option(help="24.3")] = None,
    output_format: Annotated[str, typer.Option(help="console|json|markdown")] = "console",
    output: Annotated[Path | None, typer.Option(help="Write report to file")] = None,
) -> None:
    """Analyze ClickHouse workload risk.

    Two modes:

      CSV:   chadvisor workload --query-log query_log.csv

      Live:  chadvisor workload --connect http://localhost:8123 --since 24h
    """
    from clickadvisor.workload.analyzer import (
        analyze_query_log_csv,
        analyze_query_log_rows,
        render_workload_json,
        render_workload_markdown,
        workload_report_to_dict,
    )

    if output_format not in {"console", "json", "markdown"}:
        raise typer.BadParameter("output_format must be one of: console, json, markdown")
    if top_n <= 0:
        raise typer.BadParameter("top_n must be positive")
    if connect and query_log:
        typer.echo("Error: use --connect OR --query-log, not both.", err=True)
        raise typer.Exit(1)
    if not connect and not query_log:
        typer.echo("Error: provide --connect <url> or --query-log <path>.", err=True)
        raise typer.Exit(1)

    if connect:
        from clickadvisor.workload.live_reader import ClickHouseLiveReader, LiveReaderConfig

        reader_cfg = LiveReaderConfig(
            url=connect,
            user=ch_user,
            password=ch_password,
            since=since,
        )
        reader = ClickHouseLiveReader(reader_cfg)

        if not reader.check_connection():
            typer.echo(f"Error: cannot reach ClickHouse at {connect}", err=True)
            raise typer.Exit(1)

        typer.echo(f"Connected to {connect}. Reading {since} from system.query_log...")
        rows = reader.fetch()

        if not rows:
            typer.echo("No query_log rows found for the given time range.")
            raise typer.Exit(0)

        report = analyze_query_log_rows(rows, source=connect, top_n=top_n, ch_version=ch_version)
    else:
        assert query_log is not None
        report = analyze_query_log_csv(query_log, top_n=top_n, ch_version=ch_version)

    if output_format == "json":
        rendered = render_workload_json(report)
    else:
        rendered = render_workload_markdown(report)

    if output is not None:
        output.write_text(rendered + "\n", encoding="utf-8")
        console.print(f"Wrote workload report to {output}")
        return

    if output_format == "json":
        console.print_json(data=workload_report_to_dict(report))
    else:
        console.print(rendered)


@app.command()
def index_kb(
    chunks_dir: Annotated[
        str,
        typer.Option(help="Директория с Markdown-чанками knowledge base"),
    ] = "data/kb/chunks",
    db_path: Annotated[
        str,
        typer.Option(help="Путь к embedded Qdrant базе"),
    ] = ".qdrant_db",
    reindex: Annotated[
        bool,
        typer.Option("--reindex", help="Пересоздать индекс"),
    ] = False,
    embedding_model: Annotated[
        str,
        typer.Option(
            help=(
                "Embedding model: multilingual-e5-small (default, multilingual) "
                "or minilm-l6 (english-only, faster, better MRR@3 on English KB)"
            )
        ),
    ] = "multilingual-e5-small",
) -> None:
    """Индексировать knowledge base для retrieval advisory."""
    from clickadvisor.retrieval.indexer import KBIndexer

    indexer = KBIndexer(db_path=db_path, embedding_model=embedding_model)
    if not reindex and indexer.is_indexed():
        typer.echo("KB уже проиндексирован. Используйте --reindex для обновления.")
        return

    with Progress() as progress:
        task = progress.add_task("Индексация KB...", total=None)
        count = indexer.reindex(chunks_dir) if reindex else indexer.index_kb(chunks_dir)
        progress.update(task, completed=1)

    typer.echo(f"Проиндексировано {count} чанков")
