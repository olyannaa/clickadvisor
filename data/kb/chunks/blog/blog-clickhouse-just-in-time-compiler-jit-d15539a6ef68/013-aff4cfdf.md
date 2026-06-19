---
source: blog
url: https://maksimkita.com/
topic: jit-in-clickhouse
ch_version_introduced: '10.3'
last_updated: '2026-06-12'
chunk_index: 13
total_chunks_in_doc: 20
---

Assume we have such DAG `plus(plus(a, multiply(b, c)), 5)`: ![actions_dag.svg](/uploads/actions_dag_dc019485f0.svg) After JIT compilation, DAG will look like this: ![actions_dag_after_compilation.svg](/uploads/actions_dag_after_compilation_2627221906.svg) Multiple functions are fused into a single function, and constants are inlined. Additionally, JIT helps us with the following:

- Improved L1, L2 cache usages.
- Less code to execute. It is placed on 1 page. Better usage of CPU branch predictor.
- Eliminate indirections.
- Multiple operations are fused in one function. The compiler can perform more optimizations.
- Using target CPU instructions (AVX256, AVX512\) if necessary. LLVM compiler can use the latest available instruction set for your CPU (AVX2, AVX512\) during compilation.

Improved usage of L1, L2 caches is important. If we check well\-known [table of numbers](http://norvig.com/21-days.html#answers), main memory reference is 20x times slower than L2 cache access, and 200x times slower that L1 cache access.

Consider such example `SELECT a + b * c + 5 FROM test_table`. This expression DAG `plus(plus(a, multiply(b, c)), 5)` is compiled into such LLVM IR:
