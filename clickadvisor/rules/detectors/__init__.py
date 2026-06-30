from clickadvisor.rules.detectors.D003_select_star import D003SelectStar
from clickadvisor.rules.detectors.D004_missing_limit import D004MissingLimit
from clickadvisor.rules.detectors.D007_final_modifier import D007FinalModifier
from clickadvisor.rules.detectors.D014_async_insert_no_wait import D014AsyncInsertNoWait
from clickadvisor.rules.detectors.D015_optimize_table_final import D015OptimizeTableFinal
from clickadvisor.rules.detectors.D016_alter_table_mutation import D016AlterTableMutation
from clickadvisor.rules.detectors.D017_nullable_column_in_ddl import D017NullableColumnInDDL
from clickadvisor.rules.detectors.D018_deprecated_ngrambf_tokenbf_index import (
    D018DeprecatedNgramBFIndex,
)
from clickadvisor.rules.detectors.D019_set_zero_unlimited_skip_index import (
    D019SetZeroUnlimitedSkipIndex,
)

__all__ = [
    "D003SelectStar",
    "D004MissingLimit",
    "D007FinalModifier",
    "D014AsyncInsertNoWait",
    "D015OptimizeTableFinal",
    "D016AlterTableMutation",
    "D017NullableColumnInDDL",
    "D018DeprecatedNgramBFIndex",
    "D019SetZeroUnlimitedSkipIndex",
]
