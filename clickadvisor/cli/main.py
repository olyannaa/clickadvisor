from __future__ import annotations

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


@app.command()
def version() -> None:
    console.print(f"ClickAdvisor {__version__}")


@app.command()
def analyze(
    sql: Annotated[Path, typer.Option(help="SQL файл")],
    explain: Annotated[Path | None, typer.Option()] = None,
    schema: Annotated[Path | None, typer.Option()] = None,
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
) -> None:
    if mode not in {"diagnose", "explain"}:
        raise typer.BadParameter("mode must be one of: diagnose, explain")
    if output_format not in {"console", "json", "markdown"}:
        raise typer.BadParameter("output_format must be one of: console, json, markdown")

    sql_text = sql.read_text(encoding="utf-8")
    explain_text = _read_optional(explain)
    schema_text = _read_optional(schema)

    version = ch_version
    if connect and not ch_version:
        version = detect_version(connect, user=ch_user, password=ch_password)

    context = QueryContext(
        sql=sql_text,
        explain_output=explain_text,
        schema_ddl=schema_text,
        ch_version=version,
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

    pipeline = AnalysisPipeline(rules, mode=mode, retrieval_advisor=retrieval_advisor)
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
def index_kb(
    chunks_dir: Annotated[
        str,
        typer.Option(help="Директория с Markdown-чанками knowledge base"),
    ] = "data/kb/chunks",
    db_path: Annotated[
        str,
        typer.Option(help="Путь к embedded Qdrant базе"),
    ] = ".qdrant_db",
) -> None:
    """Индексировать knowledge base для retrieval advisory."""
    from clickadvisor.retrieval.indexer import KBIndexer

    indexer = KBIndexer(db_path=db_path)
    with Progress() as progress:
        task = progress.add_task("Индексация KB...", total=None)
        count = indexer.index_kb(chunks_dir)
        progress.update(task, completed=1)

    typer.echo(f"Проиндексировано {count} чанков")
