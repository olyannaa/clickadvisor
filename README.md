<p align="center">
  <img src="docs/demo.png" alt="ClickAdvisor CLI demo" width="760">
</p>

<h1 align="center">ClickAdvisor</h1>

<p align="center">
  Local-first ClickHouse Performance Advisor для SQL, workload и AI-agent workflow.
</p>

<p align="center">
  <a href="README.md"><img alt="README Russian" src="https://img.shields.io/badge/README-Русский-2ea44f?style=for-the-badge"></a>
  <a href="README.en.md"><img alt="README English" src="https://img.shields.io/badge/README-English-0969da?style=for-the-badge"></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="ClickHouse" src="https://img.shields.io/badge/ClickHouse-performance%20advisor-ffcc01">
  <img alt="MCP" src="https://img.shields.io/badge/MCP-stdio%20%2B%20HTTP-blueviolet">
  <img alt="Local First" src="https://img.shields.io/badge/security-local--first-success">
</p>

ClickAdvisor помогает DBA, data engineers, backend engineers и platform-командам
находить рискованные ClickHouse SQL-паттерны до production-инцидентов,
перерасхода CPU/RAM и дорогих cloud-счетов.

Это не generic SQL chatbot. Trusted runtime построен вокруг deterministic
ClickHouse rule engine: каждое срабатывание имеет `rule_id`, severity, tier,
confidence, объяснение и rewrite-пример там, где rewrite безопасен. AI
используется как интерфейс через MCP и как исследовательский workflow, но не как
источник production-рекомендаций.

## Содержание

- [Что умеет](#что-умеет)
- [Быстрый старт](#быстрый-старт)
- [Single-query advisor](#single-query-advisor)
- [Workload analyzer](#workload-analyzer)
- [MCP](#mcp)
- [Data Science и ML](#data-science-и-ml)
- [Evaluation](#evaluation)
- [Security](#security)
- [Документация](#документация)

## Что умеет

| Поверхность | Возможность |
|---|---|
| SQL advisor | Анализ одного ClickHouse SQL через CLI, JSON, Markdown или MCP |
| Rule engine | 119 ClickHouse-specific правил, detectors и environment checks |
| Workload analyzer | `system.query_log` CSV/live анализ, normalized fingerprints, top-N risks |
| EXPLAIN ESTIMATE | Planner rows/marks comparison без выполнения пользовательского запроса |
| MCP server | Local stdio MCP и Streamable HTTP MCP для remote-compatible demo |
| Local retrieval | Embedded Qdrant KB по ClickHouse docs, Altinity KB, blog/release notes |
| DS/ML lab | Expert dataset, EDA, features, group split, baselines, error analysis |

## Почему это важно для ClickHouse

ClickHouse быстро выполняет аналитические запросы, но performance зависит от
деталей движка: MergeTree, sparse primary key, marks/parts, `FINAL`, skip
indexes, `PREWHERE`, materialized views, distributed execution, memory/thread
settings и реального workload.

ClickAdvisor закрывает практическую задачу: не “угадать оптимизацию”, а дать
проверяемый ClickHouse-specific сигнал, который можно показать DBA, положить в
CI, передать AI-агенту через MCP или использовать для workload review queue.

## Быстрый старт

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor analyze --sql query.sql
```

Docker:

```bash
docker build -t clickadvisor .
docker run --rm -p 8000:8000 clickadvisor
```

По умолчанию Docker image поднимает lightweight Streamable HTTP MCP endpoint
на `/mcp`. Образ предназначен для demo/deploy сценария и не ставит тяжёлые
ML/retrieval зависимости.

## Single-query Advisor

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --ch-version 25.3 \
  --output-format markdown \
  --no-retrieval
```

Пример рискованного запроса:

```sql
SELECT
    e.country,
    COUNT(DISTINCT e.user_id) AS unique_users,
    sumIf(e.revenue, e.status = 'paid') AS paid_revenue
FROM
(
    SELECT *
    FROM events FINAL
    WHERE message LIKE '%timeout%'
      AND (country = 'RU' OR country = 'KZ' OR country = 'BY')
) AS e
JOIN users AS u
    ON toUInt64(e.user_id) = u.id
GROUP BY e.country
HAVING e.country = 'RU'
ORDER BY paid_revenue DESC;
```

На этом запросе ClickAdvisor находит 10 срабатываний, включая:

- `R-001`: `COUNT(DISTINCT user_id)` -> `uniqExact(user_id)`;
- `R-002`: approximate distinct через `uniq`, если это допустимо;
- `D-005` / `R-102`: leading wildcard search и skip-index/search strategy;
- `D-007`: дорогой `FINAL` на MergeTree;
- `D-011`, `R-008`, `R-020`: приведение типов вокруг JOIN/filter keys;
- `R-011`: non-aggregate `HAVING` можно перенести в `WHERE`;
- `R-014`: дорогой `GROUP BY` по строковой колонке.

<p align="center">
  <img src="docs/assets/readme-example-output.svg" alt="ClickAdvisor markdown report example" width="780">
</p>

## Workload Analyzer

CSV export из `system.query_log`:

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format markdown \
  --top-n 3
```

Live read-only режим через ClickHouse HTTP API:

```bash
poetry run chadvisor workload \
  --connect http://localhost:8123 \
  --user default \
  --password secret \
  --since 24h \
  --output-format markdown \
  --top-n 10
```

`workload` группирует похожие запросы по normalized fingerprint, считает
executions, total/avg/p95 latency, read rows/bytes и memory usage, затем
прогоняет representative SQL через rule engine и формирует top-N DBA review
queue.

Пример top risk из sample:

```text
Priority: high
Executions: 2
Total duration: 2180 ms
Read bytes: 350000000
Rule IDs: D-003, D-004, D-005, D-007, R-102
Normalized SQL: select * from events final where message like ?
```

Подробнее: [docs/workload.md](docs/workload.md).

## MCP

Локальный stdio MCP для Claude Desktop, Cursor, Zed и других MCP-клиентов:

```bash
poetry run chadvisor mcp-server
```

Публичный MCP endpoint для проверки без локальной установки:

```text
https://clickadvisor-mcp-production.up.railway.app/mcp
```

В Claude / Anthropic API remote MCP подключается как URL-based server:

```text
Claude / Claude Desktop:
Customize -> Connectors -> Add custom connector
Name: ClickAdvisor
URL:  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Claude Code:

```bash
claude mcp add --transport http clickadvisor \
  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Anthropic API:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "name": "clickadvisor",
      "url": "https://clickadvisor-mcp-production.up.railway.app/mcp"
    }
  ]
}
```

Доступные MCP tools:

| Tool | Назначение |
|---|---|
| `analyze_query` | Markdown-отчёт по ClickHouse SQL |
| `analyze_query_json` | Структурированный JSON для автоматизации |
| `list_rules` | Список зарегистрированных правил |
| `detect_ch_version` | Определение версии ClickHouse через HTTP API |

Если открыть `/mcp` в браузере, можно увидеть ошибку `Not Acceptable: Client
must accept text/event-stream`. Это нормально: endpoint предназначен для MCP
clients, а не для обычной HTML-страницы.

Подробнее:

- [docs/MCP.md](docs/MCP.md)
- [docs/mcp-deployment.md](docs/mcp-deployment.md)
- [docs/ai-mcp-workflow.md](docs/ai-mcp-workflow.md)

## Schema, EXPLAIN и Environment

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --schema schema.sql \
  --explain explain.json \
  --environment environment.json
```

Environment context включает настройки, hardware, cluster и workload facts для
`E-*` и части Tier 2 advisory rules:

```json
{
  "settings": {
    "max_threads": 64,
    "max_memory_usage": 90000000000,
    "join_use_nulls": true
  },
  "hardware": {
    "cpu_cores": 16,
    "ram_bytes": 128000000000,
    "disk_type": "hdd"
  },
  "workload": {
    "interactive_queries": true,
    "large_join": true,
    "bulk_inserts": true
  },
  "cluster": {
    "shards": 4,
    "replicas": 2
  }
}
```

EXPLAIN ESTIMATE:

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --connect http://localhost:8123 \
  --ch-user default \
  --ch-password secret \
  --explain-estimate
```

ClickAdvisor выполняет только `EXPLAIN ESTIMATE`, не запускает пользовательский
запрос и не читает result data.

## Data Science и ML

DS-часть нужна не для замены rule engine. Её задача — формализовать качество,
сравнить подходы, найти ограничения и подготовить triage/prioritization layer.

Expert dataset:

| Показатель | Значение |
|---|---:|
| SQL records | 20 235 |
| Real / synthetic | 19 090 / 1 145 |
| Successful local replay records | 9 837 |
| Final labels | low 4 253 / medium 14 285 / high 1 697 |
| Numeric feature count | 115 |
| Rule vocabulary | 54 |

Ключевой факт по источнику меток:

| Label source | Records | Интерпретация |
|---|---:|---|
| `rule_only` | 14 693 | модель в основном учит compressed rule-engine signal |
| `measured_only` | 4 635 | независимый сигнал из latency/read/memory |
| `both` | 907 | самый надёжный core, где static и measured signals согласны |

Baseline ladder:

| Model | CV macro-F1 | Holdout macro-F1 |
|---|---:|---:|
| Dummy most frequent | 0.275 +/- 0.000 | 0.278 |
| Dummy stratified | 0.328 +/- 0.009 | 0.335 |
| TF-IDF + Logistic Regression | 0.864 +/- 0.011 | 0.882 |
| Structural/rule LR | 0.827 +/- 0.004 | 0.837 |
| Random Forest all features | 0.938 +/- 0.006 | 0.949 |
| CatBoost tabular | 0.873 +/- 0.008 | 0.871 |

Holdout error analysis для Random Forest:

| Slice | Records | Macro-F1 | High recall |
|---|---:|---:|---:|
| all_holdout | 3 039 | 0.949 | 0.887 |
| rule_only | 2 235 | 0.970 | 0.990 |
| measured_only | 672 | 0.595 | 0.785 |
| both | 132 | 0.975 | 1.000 |

Вывод: ML полезен для triage, confidence grouping и review queue ordering, но
production-рекомендации остаются rule-first.

Подробнее:

- [docs/evaluation.md](docs/evaluation.md)
- [docs/experiments/risk_labeling_ds_summary.md](docs/experiments/risk_labeling_ds_summary.md)
- [data/ml/expert_dataset/eda/ds_report.md](data/ml/expert_dataset/eda/ds_report.md)

## Evaluation

| Evaluation surface | Data | Result |
|---|---|---:|
| Rule detection | 222 synthetic/schema/env cases | precision 1.000 / recall 1.000 / F1 1.000 |
| Retrieval | 20 query -> docs pairs | best MRR@3 0.517 |
| Risk-label DS | 20 235 SQL records | RF holdout macro-F1 0.949 |
| Workload prototype | sample query_log CSV | normalized groups + top-N risk report |

Воспроизводимые проверки:

```bash
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run pytest --ignore=tests/integration -q
poetry run python scripts/rules/validate_catalog.py
poetry run python scripts/benchmark/validate_cases.py
poetry run python scripts/eval/run_benchmark.py --cases-dir benchmark/cases/synthetic_expanded --mode strict
```

## Security

ClickAdvisor можно запускать внутри компании, CI/CD или локальной среды
инженера без отправки SQL, DDL, EXPLAIN, environment context и query_log во
внешние LLM/API.

Что может читать ClickAdvisor:

- SQL text;
- optional schema DDL;
- optional EXPLAIN output;
- optional environment JSON;
- sanitized `system.query_log` CSV или read-only live metadata;
- `SELECT version()` при version detection;
- `EXPLAIN ESTIMATE` только при явном флаге.

Что он не делает по умолчанию:

- не выполняет пользовательский SQL для speedup measurement;
- не читает result data;
- не выполняет `ANALYZE`;
- не применяет DDL/mutations;
- не делает hidden remote LLM calls.

Подробнее: [docs/security-local-first.md](docs/security-local-first.md).

## Документация

- [Architecture](docs/ARCHITECTURE.md)
- [Evaluation](docs/evaluation.md)
- [Workload Analyzer](docs/workload.md)
- [MCP](docs/MCP.md)
- [MCP Deployment](docs/mcp-deployment.md)
- [Security / Local-First](docs/security-local-first.md)
- [Rule Catalog](docs/rules/README.md)

## License

MIT
