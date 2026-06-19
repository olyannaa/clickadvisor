import typer
from rich.console import Console
from rich.table import Table

from clickadvisor import __version__

app = typer.Typer(
    help="Local-first CLI advisor for ClickHouse query optimization.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Print the current ClickAdvisor version."""
    console.print(f"ClickAdvisor {__version__}")


@app.command()
def doctor(llm: str = typer.Option("none", help="none, local, or remote")) -> None:
    """Show the fixed product assumptions for the current build."""
    table = Table(title="ClickAdvisor MVP profile")
    table.add_column("Dimension")
    table.add_column("Value")
    table.add_row("Engine", "ClickHouse only")
    table.add_row("Primary interface", "CLI")
    table.add_row("Rules", "Tier 1, Tier 2, Tier 3")
    table.add_row("LLM mode", llm)
    table.add_row("Execution model", "Local-first, no customer SQL leaves host by default")
    table.add_row("Data access", "SQL, EXPLAIN, schema, metadata, config, hardware spec")
    console.print(table)
