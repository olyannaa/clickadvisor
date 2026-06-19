## ClickAdvisor Report

### Finding F-001

- Type: `env_suggestion`
- Scope: `query_parallelism`
- Severity: `medium`

The supplied hardware profile suggests fewer effective execution lanes than the
observed pipeline fan-out. Review `max_threads` in the relevant profile before
assuming the query itself is the only bottleneck.
