from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

from clickadvisor.core.models import QueryContext
from clickadvisor.core.pipeline import AnalysisPipeline
from clickadvisor.rules.registry import get_applicable_rules

BENCHMARK_ROOT = Path("benchmark/cases/synthetic")
console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ClickAdvisor synthetic benchmark.")
    parser.add_argument(
        "--mode",
        default="lenient",
        choices=["strict", "lenient"],
        help="Evaluation mode: exact set match or expected-coverage mode.",
    )
    return parser.parse_args()


def load_cases(root: Path = BENCHMARK_ROOT) -> list[dict]:
    cases: list[dict] = []
    for path in sorted(root.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            cases.append(payload)
    return cases


def run_case(case: dict, mode: str) -> dict:
    context = QueryContext(sql=case["sql"])
    rules = get_applicable_rules(None)
    pipeline = AnalysisPipeline(rules)
    report = pipeline.run(context)

    found = {finding.rule_id for finding in report.findings}
    expected = set(case["expected_rules_to_fire"])

    tp = found & expected
    fn = expected - found
    fp = found - expected if mode == "strict" else set()

    return {
        "case_id": case["case_id"],
        "found": found,
        "expected": expected,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def compute_metrics(results: list[dict]) -> tuple[float, float, float]:
    tp_total = sum(len(result["tp"]) for result in results)
    fp_total = sum(len(result["fp"]) for result in results)
    fn_total = sum(len(result["fn"]) for result in results)

    precision = tp_total / (tp_total + fp_total) if tp_total + fp_total else 0.0
    recall = tp_total / (tp_total + fn_total) if tp_total + fn_total else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def build_rule_stats(results: list[dict]) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {"tp": 0, "fp": 0, "fn": 0, "expected": 0, "found": 0}
    )

    for result in results:
        for rule_id in result["expected"]:
            stats[rule_id]["expected"] += 1
        for rule_id in result["found"]:
            stats[rule_id]["found"] += 1
        for rule_id in result["tp"]:
            stats[rule_id]["tp"] += 1
        for rule_id in result["fp"]:
            stats[rule_id]["fp"] += 1
        for rule_id in result["fn"]:
            stats[rule_id]["fn"] += 1

    return dict(sorted(stats.items()))


def print_overall(results: list[dict], mode: str) -> None:
    precision, recall, f1 = compute_metrics(results)
    console.print(f"[bold]Synthetic benchmark results ({mode})[/bold]")
    console.print(f"Cases: {len(results)}")
    console.print(f"Overall precision: {precision:.3f}")
    console.print(f"Overall recall:    {recall:.3f}")
    console.print(f"Overall F1:        {f1:.3f}")


def print_rule_table(rule_stats: dict[str, dict[str, int]], mode: str) -> None:
    table = Table(title=f"Per-rule precision/recall ({mode})")
    table.add_column("Rule")
    table.add_column("TP", justify="right")
    table.add_column("FP", justify="right")
    table.add_column("FN", justify="right")
    table.add_column("Found", justify="right")
    table.add_column("Expected", justify="right")
    table.add_column("Precision", justify="right")
    table.add_column("Recall", justify="right")

    for rule_id, stats in rule_stats.items():
        tp = stats["tp"]
        fp = stats["fp"]
        fn = stats["fn"]
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        table.add_row(
            rule_id,
            str(tp),
            str(fp),
            str(fn),
            str(stats["found"]),
            str(stats["expected"]),
            f"{precision:.2f}",
            f"{recall:.2f}",
        )

    console.print(table)


def print_case_mismatches(results: list[dict], mode: str) -> None:
    mismatches = [result for result in results if result["fp"] or result["fn"]]
    if not mismatches:
        console.print(f"[green]No mismatches across synthetic cases ({mode}).[/green]")
        return

    table = Table(title=f"Case mismatches ({mode})")
    table.add_column("Case")
    table.add_column("Expected")
    table.add_column("Found")
    table.add_column("FP")
    table.add_column("FN")

    for result in mismatches:
        table.add_row(
            result["case_id"],
            ", ".join(sorted(result["expected"])) or "—",
            ", ".join(sorted(result["found"])) or "—",
            ", ".join(sorted(result["fp"])) or "—",
            ", ".join(sorted(result["fn"])) or "—",
        )

    console.print(table)


def main() -> None:
    args = parse_args()
    cases = load_cases()
    results = [run_case(case, mode=args.mode) for case in cases]
    rule_stats = build_rule_stats(results)
    print_overall(results, mode=args.mode)
    print_rule_table(rule_stats, mode=args.mode)
    print_case_mismatches(results, mode=args.mode)


if __name__ == "__main__":
    main()
