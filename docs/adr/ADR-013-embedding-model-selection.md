# ADR-013: Embedding Model Selection

Status: Accepted

## Context

Ablation experiment сравнил три embedding модели на 20 синтетических кейсах
(MRR@3 метрика, 500 KB чанков):

- multilingual-e5-small: MRR@3=0.38, 117 MB, multilingual
- all-MiniLM-L6-v2: MRR@3=0.53, 80 MB, english-only
- paraphrase-multilingual-MiniLM-L12-v2: MRR@3=0.30, 420 MB, multilingual

## Decision

Дефолтная модель — multilingual-e5-small, несмотря на более низкий MRR@3 на
английском KB. Причины:

1. KB будет пополняться русскоязычными источниками (YouTube транскрипты,
   русские чаты DBA, Stack Overflow на русском)
2. Пользователи могут задавать запросы на русском
3. Разница в MRR@3 (0.38 vs 0.53) приемлема для advisory компонента, который
   является дополнительным слоем, а не основным

all-MiniLM-L6-v2 доступна через флаг `--embedding-model minilm-l6` для
английских окружений.

## Consequences

- Retrieval качество для чисто английских установок можно улучшить флагом
  `--embedding-model minilm-l6`
- При добавлении русскоязычных источников в KB преимущество
  multilingual-e5-small возрастёт


## Follow-up

The ablation script now indexes the first 2000 KB chunks for routine local
comparison and prints a footnote noting the full 8804-chunk KB size. The decision
above remains unchanged: `multilingual-e5-small` is the default for multilingual
coverage, and `minilm-l6` remains an opt-in model for English-only deployments.
