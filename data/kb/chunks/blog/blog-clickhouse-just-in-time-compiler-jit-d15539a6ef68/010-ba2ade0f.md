---
source: blog
url: https://maksimkita.com/
topic: jit-in-clickhouse
ch_version_introduced: '10.3'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 20
---

Float64 Float32 Float64 ``` specializations for different types. And in addition, specializations if one of the columns is a constant column. In result 20 x 20 \= 400 specializations for single `plus` function. Advantages of the current interface:

- Code isolation. Inside a function, it is easy to implement some complex operations or make nontrivial logic. It will be well isolated inside the function.
- High efficiency. Specializations for different types can be generated using templates.
- Compiler can vectorize loops using SIMD instructions. As said before, columns are just arrays, so most functions iterate over arrays and apply some operation.

Disadvantages:

- Heavy template usage. For some functions, templates can become complex.
- Binary code bloat. Mostly it is related to heavy template usage.
- AVX256, AVX512 instructions cannot be used without runtime dispatch using CPUID, because ClickHouse is distributed as a portable binary with minimum instruction set SSE4\.2\.

Now let’s discuss Clickhouse query execution. ClickHouse query execution from a high level looks like this:

1. Parse query into AST.
2. Make AST optimizations (Most need to be moved into optimizations on logical query plan).
3. Build a logical query plan \+ make logical query plan optimizations.
4. Build a physical query plan \+ make physical query plan optimizations.
5. Execute physical query plan.

And we can easily introspect the output of each step using EXPLAIN query.

Explain AST:

```
EXPLAIN AST value * 2 + 1 FROM test_table
WHERE value > 10 ORDER BY value;

┌─explain─────────────────────────────────────┐
│ SelectWithUnionQuery (children 1)           │
│  ExpressionList (children 1)                │
│   SelectQuery (children 4)                  │
│    ExpressionList (children 1)              │
│     Function plus (children 1)              │
│      ExpressionList (children 2)            │
│       Function multiply (children 1)        │
│        ExpressionList (children 2)          │
│         Identifier value                    │
│         Literal UInt64_2                    │
│       Literal UInt64_1                      │
│    TablesInSelectQuery (children 1)         │
│     TablesInSelectQueryElement (children 1) │
│      TableExpression (children 1)           │
│       TableIdentifier test_table            │
│    Function greater (children 1)            │
│     ExpressionList (children 2)             │
│      Identifier value                       │
│      Literal UInt64_10                      │
│    ExpressionList (children 1)              │
│     OrderByElement (children 1)             │
│      Identifier value                       │
└─────────────────────────────────────────────┘

```

Explain logical query plan:
