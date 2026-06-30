from clickadvisor.rules.detectors.backlog import (
    D001FullScanOnPartitionedTable,
    D002CrossJoinRisk,
    D005LeadingWildcardLike,
    D006ArrayJoinBeforeFilter,
    D008SampleWithoutSampleBy,
    D009NullableWithoutNeed,
    D010UnusedColumnsInSelect,
    D011ImplicitTypeCoercionInJoin,
    D012WindowFunctionWithoutPartition,
    D013DeeplyNestedSubqueries,
)
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
from clickadvisor.rules.detectors.D020_partition_by_non_date import D020PartitionByNonDate
from clickadvisor.rules.detectors.D021_select_star_in_mv import D021SelectStarInMV
from clickadvisor.rules.detectors.D022_delete_without_where import D022DeleteWithoutWhere
from clickadvisor.rules.detectors.D023_mv_without_to import D023MVWithoutTo
from clickadvisor.rules.detectors.D024_mv_with_populate import D024MVWithPopulate
from clickadvisor.rules.detectors.D025_mv_with_join import D025MVWithJoin

__all__ = [
    "D003SelectStar",
    "D001FullScanOnPartitionedTable",
    "D002CrossJoinRisk",
    "D005LeadingWildcardLike",
    "D006ArrayJoinBeforeFilter",
    "D008SampleWithoutSampleBy",
    "D009NullableWithoutNeed",
    "D010UnusedColumnsInSelect",
    "D011ImplicitTypeCoercionInJoin",
    "D012WindowFunctionWithoutPartition",
    "D013DeeplyNestedSubqueries",
    "D004MissingLimit",
    "D007FinalModifier",
    "D014AsyncInsertNoWait",
    "D015OptimizeTableFinal",
    "D016AlterTableMutation",
    "D017NullableColumnInDDL",
    "D018DeprecatedNgramBFIndex",
    "D019SetZeroUnlimitedSkipIndex",
    "D020PartitionByNonDate",
    "D021SelectStarInMV",
    "D022DeleteWithoutWhere",
    "D023MVWithoutTo",
    "D024MVWithPopulate",
    "D025MVWithJoin",
]
