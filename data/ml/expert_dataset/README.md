# ClickAdvisor Expert SQL Dataset

Воспроизводимый JSONL-корпус из реальных ClickHouse SQL benchmark/test источников и контролируемых antipattern-вариантов.

- Записей: 20235
- Реальных записей: 19090
- Синтетических записей: 1145
- Метод статической разметки: benchmark expected rules plus feature-derived weak labels.
- Метод measured-разметки: локальный replay в ClickHouse 25.3 через `system.query_log`.

Файлы:

- `queries.jsonl` - одна нормализованная запись запроса на строку.
- `manifest.json` - счетчики по источникам, risk-классам, правилам и metadata сборки.

Поле `measured_metrics` заполнено для всех записей: успешные read-only запросы имеют
статус `ok`, невыполнимые в локальной схеме запросы имеют статус `error`,
небезопасные для replay `INSERT`/`CREATE` записи имеют статус `skipped`.
Поля `rule_findings`, `rule_ids`, `rule_max_severity`, `rule_max_tier` и
`rule_risk_label` заполнены полным прогоном ClickAdvisor rule engine через
`poetry run python scripts/lab/label_dataset.py`.
Поля `measured_risk_label`, `final_risk_label`, `label_source` и
`risk_signal_disagreement` заполнены через
`poetry run python scripts/lab/reconcile_risk_labels.py`.

EDA-артефакты:

- `eda/measured_metrics_eda.md` - распределения measured metrics, percentiles и log-гистограммы.
- `eda/label_eda.md` - class balance, source breakdown, top rules и rule co-occurrence.
- `eda/ds_report.md` - методологический отчет по labels, features, split и baseline ladder.
- `eda/risk_error_analysis/error_analysis.md` - holdout error analysis по `high`, `measured_only` и `both`.

ML-артефакты:

- `features/features.jsonl` - training feature store: normalized SQL, structural фичи и rule-derived фичи.
- `features/feature_manifest.json` - список фичей, rule vocabulary, label/source counts.
- `splits/risk_split_v1.json` - group-aware train/test/holdout split и 5 validation folds.
- `eval/results/risk_baseline_ladder_current/` - baseline ladder метрики и confusion matrices.

Локальный ClickHouse для replay поднимается командой `docker compose up -d clickhouse`,
после чего базовые таблицы и проверка `system.query_log` готовятся через
`poetry run python scripts/ml/prepare_local_clickhouse.py`.
