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

Главный принцип проекта: **rules + ML + retrieval**, где доверенное ядро
анализа остаётся rule engine с явно описанными условиями применимости. ML
используется как отдельная evaluation surface, retrieval добавляет локальные
ссылки на документацию, а утилита не отправляет SQL во внешние сервисы.

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
- 62 rewrite/advisory-правил `R-*`;
- 15 детекторов антипаттернов `D-*`;
- version detection через ClickHouse HTTP API;
- console / JSON / Markdown отчёты;
- режим объяснений `--mode explain`;
- optional retrieval advisory через embedded Qdrant KB;
- optional `EXPLAIN ESTIMATE` сравнение через ClickHouse HTTP API;
- synthetic benchmark для проверки срабатывания правил.

В каталоге `/docs/rules/cards/` описаны 119 валидируемых карточек правил:
77 из них уже имеют реализацию и тесты, 42 остаются backlog-карточками для
следующих итераций.

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

Текущий каталог:

| Surface | Карточки | Реализовано и протестировано | Backlog |
|---|---:|---:|---:|
| `R-*` rewrite/advisory rules | 74 | 62 | 12 |
| `D-*` detectors | 25 | 15 | 10 |
| `E-*` environment cards | 20 | 0 | 20 |
| Всего | 119 | 77 | 42 |

Реализованные диапазоны: `R-001`…`R-062`,
`D-003`, `D-004`, `D-007`, `D-014`…`D-025`. Карточки `R-101`…`R-112`,
`D-001`, `D-002`, `D-005`…`D-013` и `E-001`…`E-020`
пока описывают backlog.

Полный список карточек хранится в [`docs/rules/cards/`](docs/rules/cards/),
а фактическая регистрация правил — в
[`clickadvisor/rules/registry.py`](clickadvisor/rules/registry.py).

Классификация tier:

- `1A` — формально эквивалентные rewrite-правила;
- `1B` — приближённые или opt-in рекомендации;
- `1C` — условные рекомендации, зависящие от схемы или контекста;
- `detector` — диагностика антипаттерна без автоматического rewrite.

## Метрики качества

Текущие воспроизводимые метрики на 2026-06-30:

- rule detection on synthetic held-out: `36/36` cases, strict precision
  `1.000`, recall `1.000`, F1 `1.000`;
- classifier on `synthetic_expanded_v1` test split: best test macro F1
  `0.691`, best test micro F1 `0.988`;
- retrieval MRR@3: `0.517` on `20` explicit query-doc pairs with MiniLM-L6
  (`0.458` for the current multilingual-e5 default).

Rule detection is a deterministic regression metric, not an ML generalization
claim. Classifier F1 is reported separately because that layer is trained.

Запуск expanded synthetic benchmark:

```bash
poetry run python scripts/eval/run_benchmark.py \
  --cases-dir benchmark/cases/synthetic_expanded \
  --mode strict
```

Classifier ablation:

```bash
poetry run python scripts/eval/ablation_classifiers.py --run-id classifier_ablation_current
```

Для retrieval есть отдельный ablation-скрипт:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

Результаты выбора embedding-модели описаны в
[`docs/adr/ADR-013-embedding-model-selection.md`](docs/adr/ADR-013-embedding-model-selection.md).
Подробная методика и текущие результаты: [`docs/evaluation.md`](docs/evaluation.md),
[`docs/experiments/classifier_ablation.md`](docs/experiments/classifier_ablation.md),
[`docs/experiments/retrieval_ablation.md`](docs/experiments/retrieval_ablation.md).

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

### AI-assisted development

Codex и Claude использовались системно в разработке: для ревью архитектурных
решений, генерации вариантов тестов, документации и проверки согласованности
плана с кодом. Они не входят в trusted runtime path ClickAdvisor: рекомендации
CLI/MCP формируются rule engine, ML evaluation surface и локальным retrieval.

## Что не заявляется как готовое в CLI v1

- продуктовый generative LLM в critical path;
- автоматический анализ `query_log`;
- автоматические DDL-изменения;
- выполнение `ANALYZE` или реальный replay запросов на данных;
- полноценные environment rules по hardware/config.

Эти направления описаны в ADR и backlog, но README отражает именно то, что
поддерживает текущий код репозитория.
