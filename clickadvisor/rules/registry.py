from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from clickadvisor.rules.base import Rule
from clickadvisor.rules.detectors import (
    D001FullScanOnPartitionedTable,
    D002CrossJoinRisk,
    D003SelectStar,
    D004MissingLimit,
    D005LeadingWildcardLike,
    D006ArrayJoinBeforeFilter,
    D007FinalModifier,
    D008SampleWithoutSampleBy,
    D009NullableWithoutNeed,
    D010UnusedColumnsInSelect,
    D011ImplicitTypeCoercionInJoin,
    D012WindowFunctionWithoutPartition,
    D013DeeplyNestedSubqueries,
    D014AsyncInsertNoWait,
    D015OptimizeTableFinal,
    D016AlterTableMutation,
    D017NullableColumnInDDL,
    D018DeprecatedNgramBFIndex,
    D019SetZeroUnlimitedSkipIndex,
    D020PartitionByNonDate,
    D021SelectStarInMV,
    D022DeleteWithoutWhere,
    D023MVWithoutTo,
    D024MVWithPopulate,
    D025MVWithJoin,
)
from clickadvisor.rules.environment import (
    E001MaxThreadsVsCpuCores,
    E002MaxMemoryUsageVsTotalRam,
    E003ExternalGroupByThreshold,
    E004MarkCacheSizing,
    E005UncompressedCacheSizing,
    E006MergeSettingsForDiskType,
    E007StoragePolicyRecommendation,
    E008JitCompilationToggle,
    E009QueryCacheForRepeatedWorkload,
    E010PartsToThrowInsertTuning,
    E011DistributedConnectionsSizing,
    E012JoinUseNullsOverhead,
    E013AsyncInsertBusyTimeoutTuning,
    E014MergeMaxBytesForLevel,
    E015OptimizeAggregationInOrder,
    E016JoinAlgorithmForLargeTables,
    E017DistributedAggregationMemoryEfficient,
    E018InputFormatForBulkInserts,
    E019PreferLocalhostReplica,
    E020MaxExecutionTimeForProtection,
)
from clickadvisor.rules.tier1 import (
    R001CountDistinct,
    R002CountDistinctApprox,
    R003QuantileExact,
    R004CountStarDistinctSubquery,
    R005ToDateEquality,
    R006ToYYYYMMRange,
    R007ToStartOfIntervalRange,
    R008RedundantCast,
    R009InSingleton,
    R010DisjunctionToIn,
    R011HavingToWhere,
    R012ConstantPredicate,
    R013LengthToEmpty,
    R014GroupByStringHash,
    R015DistinctAfterGroupBy,
    R016OrderByWithoutLimit,
    R017SubqueryFilterPushdown,
    R018UnionToUnionAll,
    R019UintNarrowing,
    R020CastOrDefault,
    R021DateTime64ZeroToDateTime,
    R022FloatMonetary,
    R023StringDatetimeColumn,
    R024StringIPColumn,
    R025OrderByTupleNoPK,
    R026SumCaseToCountIf,
    R027SumCaseColToSumIf,
    R028CoalesceToIfNull,
    R029LowerLikeToILike,
    R030NotInSingleton,
    R031StringUUIDColumn,
    R032Int8BooleanColumn,
    R033MaxCaseToMaxIf,
    R034MinCaseToMinIf,
    R035AvgCaseToAvgIf,
    R036NestedIfToMultiIf,
    R037EmptyStringEqToEmpty,
    R038NonEmptyStringNeqToNotEmpty,
    R039LengthGteOneToNotEmpty,
    R040TodateComparisonToDatetime,
    R041StringCodeColumn,
    R042GroupArrayNoLimit,
    R043HavingCountGtZero,
    R044ToDateTimeToDateToStartOfDay,
    R045LikeWithoutWildcardsToEq,
    R046NotEmptyToNotEmpty,
    R047PositionToLike,
    R048PositionCIToILike,
    R049SumIfOneToCountIf,
    R050ToYYYYMMComparison,
    R051DateTruncToNative,
    R052FormatDateTimeYMD,
    R053ArrayReduceSum,
    R054ArrayReduceMax,
    R055ArrayReduceMin,
    R056ExtractToNative,
    R057ExtractMonthToMonth,
    R058ExtractDayToDayOfMonth,
    R059ExtractHourToHour,
    R060HasAndHasToHasAll,
    R061HasOrHasToHasAny,
    R062ArrayCountZeroToNotHas,
)
from clickadvisor.rules.tier2 import (
    R101OrderByKeyRedesign,
    R102SkipIndexRecommendation,
    R103ProjectionRecommendation,
    R104PrimaryKeyRefinement,
    R105PartitionStrategyAdjustment,
    R106LowCardinalityConversion,
    R107CodecRecommendation,
    R108PrewhereInjection,
    R109JoinReorderSmallOnRight,
    R110JoinAlgorithmChoice,
    R111MaterializedViewRecommendation,
    R112GroupByMultipassSplit,
)

DEFAULT_CARDS_DIR = Path("docs/rules/cards")
RULES = [
    R001CountDistinct(),
    R002CountDistinctApprox(),
    R003QuantileExact(),
    R004CountStarDistinctSubquery(),
    R005ToDateEquality(),
    R006ToYYYYMMRange(),
    R007ToStartOfIntervalRange(),
    R008RedundantCast(),
    R009InSingleton(),
    R010DisjunctionToIn(),
    R011HavingToWhere(),
    R012ConstantPredicate(),
    R013LengthToEmpty(),
    R014GroupByStringHash(),
    R015DistinctAfterGroupBy(),
    R016OrderByWithoutLimit(),
    R017SubqueryFilterPushdown(),
    R018UnionToUnionAll(),
    R019UintNarrowing(),
    R020CastOrDefault(),
    R021DateTime64ZeroToDateTime(),
    R022FloatMonetary(),
    R023StringDatetimeColumn(),
    R024StringIPColumn(),
    R025OrderByTupleNoPK(),
    R026SumCaseToCountIf(),
    R027SumCaseColToSumIf(),
    R028CoalesceToIfNull(),
    R029LowerLikeToILike(),
    R030NotInSingleton(),
    R031StringUUIDColumn(),
    R032Int8BooleanColumn(),
    D001FullScanOnPartitionedTable(),
    D002CrossJoinRisk(),
    D003SelectStar(),
    D004MissingLimit(),
    D005LeadingWildcardLike(),
    D006ArrayJoinBeforeFilter(),
    D007FinalModifier(),
    D008SampleWithoutSampleBy(),
    D009NullableWithoutNeed(),
    D010UnusedColumnsInSelect(),
    D011ImplicitTypeCoercionInJoin(),
    D012WindowFunctionWithoutPartition(),
    D013DeeplyNestedSubqueries(),
    D014AsyncInsertNoWait(),
    D015OptimizeTableFinal(),
    D016AlterTableMutation(),
    D017NullableColumnInDDL(),
    D018DeprecatedNgramBFIndex(),
    D019SetZeroUnlimitedSkipIndex(),
    D020PartitionByNonDate(),
    D021SelectStarInMV(),
    D022DeleteWithoutWhere(),
    D023MVWithoutTo(),
    D024MVWithPopulate(),
    D025MVWithJoin(),
    R033MaxCaseToMaxIf(),
    R034MinCaseToMinIf(),
    R035AvgCaseToAvgIf(),
    R036NestedIfToMultiIf(),
    R037EmptyStringEqToEmpty(),
    R038NonEmptyStringNeqToNotEmpty(),
    R039LengthGteOneToNotEmpty(),
    R040TodateComparisonToDatetime(),
    R041StringCodeColumn(),
    R042GroupArrayNoLimit(),
    R043HavingCountGtZero(),
    R044ToDateTimeToDateToStartOfDay(),
    R045LikeWithoutWildcardsToEq(),
    R046NotEmptyToNotEmpty(),
    R047PositionToLike(),
    R048PositionCIToILike(),
    R049SumIfOneToCountIf(),
    R050ToYYYYMMComparison(),
    R051DateTruncToNative(),
    R052FormatDateTimeYMD(),
    R053ArrayReduceSum(),
    R054ArrayReduceMax(),
    R055ArrayReduceMin(),
    R056ExtractToNative(),
    R057ExtractMonthToMonth(),
    R058ExtractDayToDayOfMonth(),
    R059ExtractHourToHour(),
    R060HasAndHasToHasAll(),
    R061HasOrHasToHasAny(),
    R062ArrayCountZeroToNotHas(),
    E001MaxThreadsVsCpuCores(),
    E002MaxMemoryUsageVsTotalRam(),
    E003ExternalGroupByThreshold(),
    E004MarkCacheSizing(),
    E005UncompressedCacheSizing(),
    E006MergeSettingsForDiskType(),
    E007StoragePolicyRecommendation(),
    E008JitCompilationToggle(),
    E009QueryCacheForRepeatedWorkload(),
    E010PartsToThrowInsertTuning(),
    E011DistributedConnectionsSizing(),
    E012JoinUseNullsOverhead(),
    E013AsyncInsertBusyTimeoutTuning(),
    E014MergeMaxBytesForLevel(),
    E015OptimizeAggregationInOrder(),
    E016JoinAlgorithmForLargeTables(),
    E017DistributedAggregationMemoryEfficient(),
    E018InputFormatForBulkInserts(),
    E019PreferLocalhostReplica(),
    E020MaxExecutionTimeForProtection(),
    R101OrderByKeyRedesign(),
    R102SkipIndexRecommendation(),
    R103ProjectionRecommendation(),
    R104PrimaryKeyRefinement(),
    R105PartitionStrategyAdjustment(),
    R106LowCardinalityConversion(),
    R107CodecRecommendation(),
    R108PrewhereInjection(),
    R109JoinReorderSmallOnRight(),
    R110JoinAlgorithmChoice(),
    R111MaterializedViewRecommendation(),
    R112GroupByMultipassSplit(),
]
RULE_REGISTRY: dict[str, Rule] = {rule.rule_id: rule for rule in RULES}


def register_rule(rule: Rule) -> Rule:
    rule_id = getattr(rule, "rule_id", "")
    if not rule_id:
        raise ValueError("rule instances must define rule_id")
    if rule_id in RULE_REGISTRY:
        raise ValueError(f"rule already registered: {rule_id}")
    RULE_REGISTRY[rule_id] = rule
    RULES.append(rule)
    return rule


def get_registered_rule(rule_id: str) -> Rule | None:
    return RULE_REGISTRY.get(rule_id)


def get_all_rules() -> list[Rule]:
    return list(RULES)


def load_rule_cards(cards_dir: Path = DEFAULT_CARDS_DIR) -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(cards_dir.rglob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        rule_id = payload.get("id")
        if isinstance(rule_id, str):
            cards[rule_id] = payload
    return cards


def get_applicable_rules(
    ch_version: str | None,
    include_skipped: bool = False,
) -> list[Rule] | tuple[list[Rule], list[str]]:
    applicable: list[Rule] = []
    skipped: list[str] = []

    for rule in RULES:
        if ch_version is None:
            applicable.append(rule)
            continue

        if rule.is_applicable_for_version(ch_version):
            applicable.append(rule)
        else:
            skipped.append(rule.rule_id)

    if include_skipped:
        return applicable, sorted(skipped)
    return applicable
