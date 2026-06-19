from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BenchmarkRunConfig:
    """Static configuration for a benchmark execution."""

    benchmark_root: Path
    results_root: Path
    llm_mode: str
    baseline_names: list[str]
    run_id: str


def discover_cases(benchmark_root: Path) -> list[Path]:
    """Return benchmark case directories in deterministic order.

    Implementation is intentionally deferred. The final version should validate
    case layout, skip disabled cases, and preserve stable ordering across runs.
    """

    raise NotImplementedError


def load_case_bundle(case_dir: Path) -> dict[str, Any]:
    """Load SQL and context artifacts for a single benchmark case.

    The final implementation should read the canonical benchmark case schema and
    prepare a normalized in-memory bundle for analyzers and baselines.
    """

    raise NotImplementedError


def run_clickadvisor_case(case_bundle: dict[str, Any], config: BenchmarkRunConfig) -> dict[str, Any]:
    """Execute ClickAdvisor on one case and return the structured report.

    The final implementation should invoke the same public analysis entry points
    used by the CLI rather than a benchmark-only code path.
    """

    raise NotImplementedError


def run_baseline_case(
    case_bundle: dict[str, Any],
    baseline_name: str,
    config: BenchmarkRunConfig,
) -> dict[str, Any]:
    """Execute one baseline system for a case and return normalized output.

    Baseline adapters should be implemented separately so that prompt templates,
    HTTP calls, and normalization logic remain version-controlled and testable.
    """

    raise NotImplementedError


def score_results(
    clickadvisor_outputs: list[dict[str, Any]],
    baseline_outputs: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Aggregate benchmark outputs into metrics and comparison tables.

    The final implementation should compute per-rule precision/recall, system
    F1, latency summaries, and Tier 2 estimated cost-reduction aggregates.
    """

    raise NotImplementedError


def persist_run_artifacts(results_root: Path, run_id: str, payload: dict[str, Any]) -> None:
    """Persist run metadata, raw outputs, and aggregated metrics.

    The final version should create `/eval/results/<run_id>/` and save metadata,
    normalized outputs, scores, and generated plots or table inputs.
    """

    raise NotImplementedError


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for benchmark execution."""

    parser = argparse.ArgumentParser(description="Run ClickAdvisor benchmark suites.")
    parser.add_argument("--benchmark-root", type=Path, default=Path("benchmark/cases"))
    parser.add_argument("--results-root", type=Path, default=Path("eval/results"))
    parser.add_argument("--llm-mode", default="none", choices=["none", "local", "remote"])
    parser.add_argument(
        "--baseline",
        action="append",
        dest="baselines",
        default=[],
        help="Baseline name to include. Can be repeated.",
    )
    parser.add_argument("--run-id", required=True, help="Unique identifier for this run.")
    return parser.parse_args()


def main() -> None:
    """Benchmark runner entry point.

    This is intentionally a skeleton only. The concrete execution flow should:

    1. discover and validate cases
    2. run ClickAdvisor across all cases
    3. run requested baselines
    4. score and compare outputs
    5. persist raw and aggregated artifacts
    """

    args = parse_args()
    config = BenchmarkRunConfig(
        benchmark_root=args.benchmark_root,
        results_root=args.results_root,
        llm_mode=args.llm_mode,
        baseline_names=args.baselines,
        run_id=args.run_id,
    )
    raise NotImplementedError(f"Benchmark runner skeleton only: {config}")


if __name__ == "__main__":
    main()
