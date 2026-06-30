# ClickAdvisor

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![ClickHouse](https://img.shields.io/badge/ClickHouse-SQL%20advisor-ffcc01)

> CLI-утилита и MCP-сервер для анализа ClickHouse SQL-запросов.
> Находит антипаттерны, предлагает rewrite-рекомендации и объясняет,
> почему рекомендация безопасна именно для ClickHouse.

ClickAdvisor помогает DBA и разработчикам быстрее разбирать медленные запросы:
он принимает SQL-файл, парсит запрос через `sqlglot`, применяет набор
детерминированных правил и возвращает отчёт в консоли, JSON или Markdown.

Главный принцип проекта: **LLM и retrieval могут помогать, но ядро анализа —
это rule engine с явно описанными условиями применимости**. Утилита работает
локально и не отправляет SQL во внешние сервисы.

[Сайт проекта](https://clickadvisor.lovable.app)

## Почему не просто ChatGPT?

ChatGPT или Claude могут дать полезную идею, но они не знают вашу версию
ClickHouse, могут опираться на устаревшие рекомендации и не всегда объясняют,
почему rewrite сохраняет смысл запроса. ClickAdvisor устроен иначе:

- каждое правило имеет `rule_id`, `tier`, версию ClickHouse и описание условий;
- version-aware фильтр скрывает правила, которые не подходят для указанной версии;
- `Tier 1A/1B/1C` отделяет доказуемые rewrite от приближённых и условных советов;
- режим `--mode explain` объясняет принцип работы ClickHouse простым языком;
- retrieval advisory добавляет ссылки на локальную knowledge base, но не заменяет rule engine.

## Статус проекта

Проект находится в активной разработке. В репозитории уже реализованы:

- CLI-команда `chadvisor analyze`;
- MCP-сервер `chadvisor mcp-server`;
- 18 Tier 1 rewrite-правил `R-001`…`R-018`;
- 3 детектора антипаттернов `D-003`, `D-004`, `D-007`;
- version detection через ClickHouse HTTP API;
- console / JSON / Markdown отчёты;
- режим объяснений `--mode explain`;
- optional retrieval advisory через embedded Qdrant KB;
- optional `EXPLAIN ESTIMATE` сравнение через ClickHouse HTTP API;
- synthetic benchmark для проверки срабатывания правил.

В каталоге `/docs/rules/cards/` описаны 54 карточки правил. Реализованная
часть в коде — 21 правило/детектор, перечисленные ниже в разделе
«Правила и покрытие».

## Быстрый старт

### Из исходников

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor analyze --sql query.sql
```

### Через pip

```bash
pip install clickadvisor
chadvisor analyze --sql query.sql
```

Пакет пока может быть не опубликован в PyPI. Надёжный способ запуска на этом
этапе — из исходников через Poetry.

### Через Docker

```bash
docker build -t clickadvisor .
docker run --rm -v "$(pwd)":/queries clickadvisor analyze --sql /queries/query.sql
```

## Пример `query.sql`

Минимальный SQL-файл — обычный ClickHouse-запрос. Например:

```sql
SELECT
    COUNT(DISTINCT user_id) AS unique_users,
    count() AS events_count
FROM events
WHERE country = 'RU'
   OR country = 'BY'
   OR country = 'KZ';
```

Что ClickAdvisor найдёт в таком запросе:

- `R-001`: `COUNT(DISTINCT user_id)` можно заменить на `uniqExact(user_id)`;
- `R-002`: если допустима приблизительная оценка, можно рассмотреть `uniq(user_id)`;
- `R-010`: цепочку `country = ... OR country = ...` можно переписать в `country IN (...)`.

Запуск:

```bash
poetry run chadvisor analyze --sql query.sql --ch-version 25.3
```

## Использование CLI

### Базовый анализ

```bash
poetry run chadvisor analyze --sql query.sql
```

Если версия ClickHouse не указана, применяются все зарегистрированные правила.
Для более точных рекомендаций лучше передавать версию явно.

### Анализ с версией ClickHouse

```bash
poetry run chadvisor analyze --sql query.sql --ch-version 25.3
```

Версия используется для фильтрации правил по `ch_version_introduced`.

### Автоопределение версии через HTTP API

```bash
poetry run chadvisor analyze --sql query.sql \
  --connect http://localhost:8123 \
  --ch-user default \
  --ch-password secret
```

ClickAdvisor выполнит только `SELECT version()` и нормализует ответ, например
`25.3.2.39` → `25.3`.

### Режим объяснений

```bash
poetry run chadvisor analyze --sql query.sql --mode explain
```

В этом режиме отчёт объясняет не только «что заменить», но и принцип работы
ClickHouse: sparse primary key index, granules, порядок выполнения `WHERE` /
`HAVING`, стоимость `FINAL`, разницу между `UNION` и `UNION ALL` и так далее.

### Форматы вывода

```bash
poetry run chadvisor analyze --sql query.sql --output-format console
poetry run chadvisor analyze --sql query.sql --output-format json
poetry run chadvisor analyze --sql query.sql --output-format markdown
```

`console` удобен для локальной диагностики, `json` — для CI/CD, `markdown` —
для PR-комментариев и MCP-ответов.

### EXPLAIN ESTIMATE

```bash
poetry run chadvisor analyze --sql query.sql \
  --connect http://localhost:8123 \
  --ch-user default \
  --ch-password secret \
  --explain-estimate
```

В этом режиме ClickAdvisor сравнивает исходный SQL и rewrite-кандидат через
`EXPLAIN ESTIMATE`. Запрос не выполняется, `ANALYZE` не запускается,
пользовательские данные не читаются. Используется только оценка планировщика
ClickHouse (`rows`, `marks`).

### Schema и EXPLAIN как дополнительные входы

CLI уже принимает опциональные файлы:

```bash
poetry run chadvisor analyze --sql query.sql \
  --schema schema.sql \
  --explain explain.json
```

На текущем этапе основная часть реализованных правил работает по SQL AST.
Схема и EXPLAIN зарезервированы для правил, которым нужен дополнительный
контекст.

## Knowledge base и retrieval advisory

Knowledge base собирается в `/data/kb/` из документации ClickHouse, Altinity KB,
ClickHouse blog и release notes. Для локального semantic search нужно
проиндексировать Markdown-чанки:

```bash
poetry run chadvisor index-kb
```

Повторная индексация:

```bash
poetry run chadvisor index-kb --reindex
```

Выбор embedding-модели:

```bash
poetry run chadvisor index-kb --embedding-model multilingual-e5-small
poetry run chadvisor index-kb --embedding-model minilm-l6
```

После индексации появится локальная директория `.qdrant_db`. Если она есть,
`analyze` по умолчанию добавляет отдельную секцию с релевантными фрагментами
документации.

Явное управление retrieval:

```bash
poetry run chadvisor analyze --sql query.sql --retrieval
poetry run chadvisor analyze --sql query.sql --no-retrieval
```

Retrieval работает локально через embeddings и Qdrant. Generative LLM не входит в critical path MVP: Claude/Cursor могут вызывать ClickAdvisor через MCP, но сами рекомендации формируются rule engine и retrieval-компонентами.

## MCP Server

ClickAdvisor можно подключить к AI-агентам как MCP-сервер:

```bash
poetry run chadvisor mcp-server
```

Пример для `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "poetry",
      "args": ["run", "chadvisor", "mcp-server"],
      "cwd": "/path/to/clickadvisor"
    }
  }
}
```

Доступные MCP tools:

- `analyze_query` — Markdown-отчёт по SQL;
- `analyze_query_json` — структурированный JSON;
- `list_rules` — список зарегистрированных правил;
- `detect_ch_version` — определение версии ClickHouse через HTTP API.

Подробности: [`docs/MCP.md`](docs/MCP.md).

## Правила и покрытие

| Rule ID | Что ищет | Tier |
|---|---|---|
| `R-001` | `COUNT(DISTINCT x)` → `uniqExact(x)` | `1A` |
| `R-002` | `COUNT(DISTINCT x)` → advisory `uniq(x)` | `1B` |
| `R-003` | `quantileExact(...)` → advisory `quantileTDigest(...)` | `1B` |
| `R-004` | `COUNT(*) FROM (SELECT DISTINCT ...)` → специализированный агрегат | `1A` |
| `R-005` | `toDate(col) = ...` → range predicate | `1A` |
| `R-006` | `toYYYYMM(...)` / `toStartOfMonth(...)` → range predicate | `1A` |
| `R-007` | `toStartOfHour/Day/FifteenMinutes(...)` → range predicate | `1A` |
| `R-008` | избыточный `CAST(...)` в фильтре | `1C` |
| `R-009` | `x IN (one_value)` → `x = one_value` | `1A` |
| `R-010` | `x = a OR x = b OR x = c` → `x IN (...)` | `1A` |
| `R-011` | условие без агрегатов в `HAVING` → `WHERE` | `1C` |
| `R-012` | `WHERE TRUE`, `AND 1=1` и другие константные предикаты | `1A` |
| `R-013` | `length(x) = 0 / > 0 / != 0` → `empty` / `notEmpty` | `1A` |
| `R-014` | advisory: hash-based `GROUP BY` для длинных строк | `1B` |
| `R-015` | лишний `DISTINCT` после эквивалентного `GROUP BY` | `1A` |
| `R-016` | `ORDER BY` в подзапросе без `LIMIT` | `1C` |
| `R-017` | pushdown внешнего фильтра во внутренний подзапрос | `1A` |
| `R-018` | advisory: `UNION` → `UNION ALL`, если множества не пересекаются | `1C` |
| `D-003` | top-level `SELECT *` | `detector` |
| `D-004` | top-level `SELECT` без `LIMIT` и без агрегации | `detector` |
| `D-007` | `FINAL` в `FROM` | `detector` |

Классификация tier:

- `1A` — формально эквивалентные rewrite-правила;
- `1B` — приближённые или opt-in рекомендации;
- `1C` — условные рекомендации, зависящие от схемы или контекста;
- `detector` — диагностика антипаттерна без автоматического rewrite.

## Метрики качества

Запуск synthetic benchmark:

```bash
poetry run python scripts/eval/run_benchmark.py
```

На синтетическом бенчмарке из 20 кейсов ожидаемые метрики в `lenient`-режиме:

- Precision: `1.00`;
- Recall: `1.00`;
- F1: `1.00`.

`lenient` означает, что дополнительные валидные находки не штрафуются, если
ожидаемые правила тоже сработали.

Для retrieval есть отдельный ablation-скрипт:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

Результаты выбора embedding-модели описаны в
[`docs/adr/ADR-013-embedding-model-selection.md`](docs/adr/ADR-013-embedding-model-selection.md).

## Архитектура

```text
SQL + optional Schema / EXPLAIN / CH version
        ↓
   SQL Parser (sqlglot, ClickHouse dialect)
        ↓
 ┌──────────────────────────────────────┐
 │  Rule Engine                         │
 │  ├─ Tier 1A: эквивалентные rewrite   │
 │  ├─ Tier 1B: opt-in / approximate    │
 │  ├─ Tier 1C: conditional rewrite     │
 │  └─ Detectors: антипаттерны          │
 └──────────────────────────────────────┘
        ↓
 Version Filter + optional EXPLAIN ESTIMATE
        ↓
 optional Retrieval Advisor (Qdrant + embeddings)
        ↓
 Report (console | JSON | Markdown | MCP)
```

Подробнее: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Безопасность и данные

ClickAdvisor не выполняет пользовательский SQL-запрос для измерения speedup.
При подключении к ClickHouse используются только:

- `SELECT version()` для определения версии;
- `EXPLAIN ESTIMATE ...` при явном флаге `--explain-estimate`.

Для базового анализа достаточно SQL-файла. Схема, EXPLAIN и подключение к
кластеру — опциональные источники контекста.

## Разработка

```bash
poetry install
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run pytest --ignore=tests/integration
poetry run python scripts/eval/run_benchmark.py
```

Integration test для version detection ожидает ClickHouse HTTP endpoint на
`localhost:8123`. В GitHub Actions он поднимается как service container.

## Что не заявляется как готовое в CLI v1

- продуктовый generative LLM в critical path;
- автоматический анализ `query_log`;
- автоматические DDL-изменения;
- выполнение `ANALYZE` или реальный replay запросов на данных;
- полноценные environment rules по hardware/config.

Эти направления описаны в ADR и backlog, но README отражает именно то, что
поддерживает текущий код репозитория.
