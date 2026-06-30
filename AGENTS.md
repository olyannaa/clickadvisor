# Правила Работы Агентов С Репозиторием

Этот файл описывает, как AI-агенты должны работать с ClickAdvisor.

## Базовый принцип

ClickAdvisor — local-first анализатор ClickHouse SQL. Доверенный runtime path:
детерминированный rule engine, ML evaluation surface и локальный retrieval.
Generative LLM не должен становиться источником production-рекомендаций внутри
CLI/MCP.

## Перед изменениями

- Начинай с чтения `README.md`, `docs/ARCHITECTURE.md`, `docs/evaluation.md` и
  релевантных файлов из `docs/rules/`.
- Проверяй текущее состояние через `git status -sb`.
- Не перетирай пользовательские изменения и не используй destructive git
  commands без явной просьбы.
- Для поиска используй `rg` / `rg --files`.

## Правила каталога

- У каждого runtime rule должен быть card в `docs/rules/cards/`.
- У каждого card со статусом implemented должна быть зарегистрированная
  реализация в `clickadvisor/rules/registry.py`.
- Нельзя добавлять duplicate `rule_id`.
- Если правилу нужен schema/environment/explain context, отсутствие контекста
  должно давать `None`, а не догадочную находку.
- Tier 2 правила являются advisory. Не добавляй automatic rewrite, если card
  явно не содержит безопасный шаблон.
- Environment rules должны читать только `QueryContext.environment` и
  дополнительные доступные context-поля.

## Тесты и benchmark

Для нового или измененного правила нужны прямые unit-тесты:

- positive case;
- no-trigger или no-context case;
- проверка ожидаемого `rule_id`.

Если правило можно представить в benchmark schema, добавь case в
`benchmark/cases/synthetic_expanded/`.

Benchmark labels должны отражать реальные multi-label overlaps. В strict mode
не должно быть неожиданных FP/FN.

## Документация

- Основная документация репозитория ведется на русском языке.
- README должен соответствовать фактическим счетчикам rules/tests/benchmark.
- Не заявляй speedup, production LLM, query replay или автоматические DDL
  изменения, если этого нет в коде и проверках.
- Enterprise/security формулировки должны подчеркивать zero data egress:
  SQL, DDL, EXPLAIN и environment context не отправляются во внешние LLM/API.

## Обязательные проверки

Перед финальным ответом или PR запускай:

```bash
poetry run python scripts/rules/validate_catalog.py
poetry run python scripts/benchmark/validate_cases.py
poetry run pytest --ignore=tests/integration -q
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run python scripts/eval/run_benchmark.py --cases-dir benchmark/cases/synthetic_expanded --mode strict
```

Если проверку невозможно запустить, явно напиши причину.

## Стиль реализации

- Следуй существующим паттернам в `clickadvisor/rules/tier1/`,
  `clickadvisor/rules/detectors/`, `clickadvisor/rules/environment.py`.
- Не добавляй тяжёлую абстракцию ради одного правила.
- Комментарии оставляй только там, где они помогают понять нетривиальную
  логику.
- Не добавляй сетевые зависимости в critical path анализа.

## Git и PR

- Работай маленькими ветками от свежего `origin/main`.
- Коммит должен быть тематически цельным.
- Перед push убедись, что рабочее дерево содержит только изменения текущей
  задачи.
