# Label EDA

- Records: 20235

## Label Counts

### rule_risk_label
- `medium`: 11057
- `low`: 8342
- `high`: 836

### measured_risk_label
- `None`: 10398
- `medium`: 4605
- `low`: 4272
- `high`: 960

### final_risk_label
- `medium`: 14285
- `low`: 4253
- `high`: 1697

### label_source
- `rule_only`: 14693
- `measured_only`: 4635
- `both`: 907

## Source by Final Label

### high
- `clickhouse_functional_tests`: 1301
- `clickhouse_performance_tests`: 170
- `clickadvisor_benchmark`: 98
- `expert_synthetic_antipatterns`: 81
- `clickbench`: 41
- `job`: 5
- `clickhouse_benchmarks_tpch`: 1

### low
- `clickhouse_functional_tests`: 3281
- `clickhouse_performance_tests`: 845
- `clickadvisor_benchmark`: 61
- `job`: 39
- `clickhouse_benchmarks_tpch`: 16
- `clickhouse_benchmarks_tpcds`: 9
- `expert_synthetic_antipatterns`: 2

### medium
- `clickhouse_functional_tests`: 12263
- `expert_synthetic_antipatterns`: 1062
- `clickhouse_performance_tests`: 810
- `job`: 69
- `clickadvisor_benchmark`: 67
- `clickhouse_benchmarks_tpcds`: 6
- `clickhouse_benchmarks_tpch`: 5
- `clickbench`: 2
- `clickhouse_bug_reproducers`: 1

## Top Rules by Final Label

### high
- `D-004`: 1024
- `D-002`: 559
- `D-003`: 247
- `R-020`: 120
- `R-008`: 107
- `R-009`: 90
- `R-001`: 51
- `R-002`: 51
- `D-006`: 46
- `R-038`: 41
- `R-011`: 29
- `D-005`: 25
- `R-102`: 25
- `R-042`: 15
- `D-010`: 14
- `R-013`: 13
- `D-007`: 13
- `R-014`: 12
- `R-005`: 12
- `R-010`: 11
- `D-012`: 8
- `D-011`: 7
- `R-004`: 7
- `R-006`: 7
- `R-007`: 7

### low
- `D-008`: 31
- `R-038`: 17
- `D-023`: 17
- `R-019`: 6
- `R-057`: 6
- `R-058`: 6
- `R-059`: 6
- `R-028`: 4
- `D-010`: 3
- `R-026`: 2
- `R-056`: 2
- `R-027`: 2
- `R-047`: 2
- `D-009`: 2
- `R-051`: 1
- `R-045`: 1
- `R-037`: 1
- `D-013`: 1

### medium
- `D-004`: 9547
- `D-003`: 1312
- `R-020`: 1042
- `R-008`: 705
- `D-007`: 510
- `D-005`: 219
- `R-102`: 219
- `R-016`: 50
- `R-038`: 44
- `D-009`: 33
- `R-042`: 30
- `R-014`: 23
- `R-003`: 17
- `D-010`: 16
- `D-012`: 15
- `D-023`: 10
- `D-013`: 9
- `R-017`: 7
- `D-024`: 7
- `D-008`: 5
- `D-021`: 5
- `R-056`: 4
- `R-028`: 4
- `R-036`: 2
- `R-049`: 2

## Top Rule Pairs

- `D-003 + D-004`: 1436
- `R-008 + R-020`: 810
- `D-004 + R-020`: 746
- `D-002 + D-004`: 430
- `D-004 + R-008`: 420
- `D-005 + R-102`: 244
- `D-004 + D-007`: 176
- `D-002 + D-003`: 143
- `D-004 + D-005`: 116
- `D-004 + R-102`: 116
- `D-003 + D-005`: 105
- `D-003 + R-102`: 105
- `D-004 + R-009`: 70
- `R-001 + R-002`: 51
- `D-003 + R-020`: 48
- `D-003 + R-008`: 41
- `D-007 + R-020`: 39
- `D-004 + D-006`: 37
- `D-003 + R-009`: 36
- `D-007 + R-008`: 34
- `D-003 + D-007`: 29
- `D-004 + D-009`: 28
- `D-004 + D-010`: 27
- `D-004 + R-016`: 27
- `D-002 + R-020`: 22
- `D-002 + R-008`: 21
- `D-007 + R-038`: 19
- `D-004 + R-042`: 18
- `D-003 + R-038`: 18
- `D-002 + D-006`: 16
