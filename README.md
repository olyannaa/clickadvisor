# ClickAdvisor

> CLI-утилита для анализа медленных ClickHouse-запросов.  
> Находит антипаттерны и предлагает формально обоснованные исправления.

## Почему не просто ChatGPT?

GPT не знает вашу точную версию ClickHouse, легко даёт устаревшие советы и не
всегда объясняет, почему конкретная рекомендация вообще должна работать.
ClickAdvisor строится вокруг формализованных правил из реляционной алгебры и
ClickHouse-specific инвариантов: каждая рекомендация привязана к rule engine,
версии ClickHouse и явному типу доверия.

## Быстрый старт

### pip

```bash
pip install clickadvisor  # placeholder, пока не опубликовано
chadvisor analyze --sql query.sql
```

### Docker

```bash
docker run --rm -v $(pwd):/queries \
  ghcr.io/username/clickadvisor:latest \
  analyze --sql /queries/query.sql
```

### Из исходников

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor analyze --sql query.sql
```

## Использование

### Базовый анализ

```bash
chadvisor analyze --sql query.sql
```

### С указанием версии CH (рекомендуется)

```bash
chadvisor analyze --sql query.sql --ch-version 25.3
```

### С подключением к кластеру (автоопределение версии)

```bash
chadvisor analyze --sql query.sql \
  --connect http://host:8123 \
  --ch-user default \
  --ch-password secret
```

### Режим объяснений (для обучения команды)

```bash
chadvisor analyze --sql query.sql --mode explain
```

### Форматы вывода

```bash
chadvisor analyze --sql query.sql --output-format json
chadvisor analyze --sql query.sql --output-format markdown
```

### CI/CD интеграция

```bash
chadvisor analyze --sql migrations/*.sql --output-format json
```

## MCP Server (для AI-агентов)

Планируемый интерфейс для MCP-клиентов:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "chadvisor",
      "args": ["mcp-server"]
    }
  }
}
```

Сейчас этот режим описан в ADR и README как целевой интерфейс; runtime-команда
`mcp-server` ещё не реализована.

## Правила и покрытие

| Rule ID | Описание | Tier |
|---|---|---|
| `R-001` | `COUNT(DISTINCT x)` → `uniqExact(x)` | `1A` |
| `R-002` | `COUNT(DISTINCT x)` → advisory `uniq(x)` | `1B` |
| `R-003` | `quantileExact(...)` → advisory `quantileTDigest(...)` | `1B` |
| `R-004` | `COUNT(*) FROM (SELECT DISTINCT ...)` collapse | `1A` |
| `R-005` | `toDate(col) = ...` → datetime range | `1A` |
| `R-006` | `toYYYYMM(...)` / `toStartOfMonth(...)` → range | `1A` |
| `R-007` | `toStartOfHour/Day/FifteenMinutes(...)` → range | `1A` |
| `R-008` | redundant `CAST(...)` in filter | `1C` |
| `R-009` | singleton `IN (...)` → equality | `1A` |
| `R-010` | `col = a OR col = b OR col = c` → `IN (...)` | `1A` |
| `R-011` | non-aggregate predicate in `HAVING` → `WHERE` | `1C` |
| `R-012` | constant predicate elimination | `1A` |
| `R-013` | `length(x) = 0 / > 0 / != 0` → `empty/notEmpty` | `1A` |
| `R-014` | advisory hash-based `GROUP BY` for long strings | `1B` |
| `R-015` | `DISTINCT` after equivalent `GROUP BY` removal | `1A` |
| `R-016` | `ORDER BY` in subquery without `LIMIT` | `1C` |
| `R-017` | subquery filter pushdown | `1A` |
| `R-018` | advisory `UNION` → `UNION ALL` | `1C` |
| `D-003` | top-level `SELECT *` detector | `detector` |
| `D-004` | missing `LIMIT` on non-aggregate top-level select | `detector` |

## Метрики качества

На курируемом бенчмарке из 20 синтетических кейсов:

- Precision: `1.00`
- Recall: `1.00`
- F1: `1.00`

Режим оценки: `lenient` (дополнительные валидные находки не штрафуются).

## Архитектура

```text
SQL + EXPLAIN + Schema
        ↓
   SQL Parser (sqlglot)
        ↓
 ┌──────────────────┐
 │  Rule Engine     │
 │  ├─ Tier 1A: formally equivalent rewrites
 │  ├─ Tier 1B: approximate rewrites (opt-in)
 │  ├─ Tier 1C: conditional rewrites
 │  └─ Detectors: antipattern detection
 └──────────────────┘
        ↓
   Version Filter (CH-specific rules)
        ↓
 Report (console | JSON | Markdown)
```

## Разработка

```bash
poetry install
poetry run pytest
poetry run python scripts/eval/run_benchmark.py
```
