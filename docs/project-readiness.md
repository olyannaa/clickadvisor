# Готовность проекта по критериям оценки

Этот документ сопоставляет текущее состояние ClickAdvisor с критериями защиты.
Формулировки намеренно evidence-based: каждый тезис опирается на код, тесты,
данные, документацию или воспроизводимые артефакты.

## Разработка

Целевой уровень: 3.

Что уже есть:

- Python package с управлением зависимостями через Poetry.
- Типизированное ядро с проверкой `mypy`.
- Линтинг через `ruff`.
- Unit tests, integration tests, validators и benchmark checks.
- GitHub Actions CI для lint/type-check/tests/ClickHouse integration.
- Docker image для Streamable HTTP MCP deployment.
- Локальное ClickHouse replay окружение через Docker Compose.
- Отдельные модули для CLI, rules, retrieval, EXPLAIN, MCP, workload и ML.

Основные проверки:

```bash
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run pytest --ignore=tests/integration -q
poetry run python scripts/rules/validate_catalog.py
poetry run python scripts/benchmark/validate_cases.py
```

Оценка: сильный уровень 3 по культуре разработки. Оставшийся production gap —
релизная упаковка для публичного распространения.

## Data Science

Целевой уровень: 3.

Что уже есть:

- Expert SQL dataset: 20 235 записей.
- Measured local replay metrics для 9 837 successful queries.
- Rule labels, measured labels, final risk labels и label-source analysis.
- EDA по measured metrics и распределениям меток.
- Feature extraction: normalized SQL, structural features, rule-derived
  features, TF-IDF внутри baselines.
- Group-aware train/test/holdout split и 5-fold validation.
- Baseline ladder: Dummy, TF-IDF + Logistic Regression, structured/rule LR,
  Random Forest, CatBoost.
- Holdout error analysis по `label_source`, особенно `measured_only` и `both`.

Ключевой результат:

- Random Forest all-features holdout macro-F1: 0.949.
- Measured-only holdout macro-F1: 0.595.
- Both-source holdout macro-F1: 0.975.

Оценка: уровень 3 по DS-контуру. Важная методологическая оговорка уже
зафиксирована: модель является triage/prioritization layer, а не заменой
детерминированного rule engine.

## Использование AI

Целевой уровень: 3.

Что уже есть:

- MCP server открывает ClickAdvisor как локальный tool для AI-клиентов.
- Local stdio MCP для desktop/IDE сценариев.
- Streamable HTTP MCP endpoint для remote-compatible demos.
- AI/MCP workflow documentation объясняет, как agents вызывают
  deterministic tools вместо генерации неподтверждённых optimization advice.
- Agent-assisted DS workflow описан как часть исследования: data preparation,
  validation, modeling и review.

Оценка: уровень 3, если на защите правильно подчеркнуть системное применение
AI-агентов. Ключевой тезис: AI является интерфейсом и ускорителем разработки,
но не trusted runtime source of recommendations.

## Продуктовое мышление

Целевой уровень: высокий 2 или 3.

Что уже есть:

- Понятные target users: DBA, data engineers, backend engineers,
  BI/dashboard owners, platform teams.
- Понятная боль: ClickHouse performance incidents, CPU/RAM waste, high latency,
  cloud cost, DBA review time.
- Competitive framing: rule-based SQL antipatterns, DB observability,
  Postgres plan advisors, learned optimizers, LLM/RAG SQL assistants.
- MVP surfaces: CLI, JSON/Markdown reports, MCP, workload analyzer, local
  retrieval, EXPLAIN ESTIMATE.
- Business-impact path: workload-level top-N opportunities и дальнейший
  impact-based ranking.

Оценка: продуктовая часть сильная для MVP. Оставшийся gap для полного уровня 3
как продуктового кейса — внешний user/market feedback: интервью, экспертная
оценка или feedback на реальном ClickHouse workload.
