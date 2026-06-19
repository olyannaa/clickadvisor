---
source: blog
url: https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library
topic: we-built-a-vector-search-engine-that-lets-you-choose-precision-at-query-time
ch_version_introduced: '0.99105519'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 14
---

is carefully designed around an auto\-vectorising algorithm, like [here](https://dl.acm.org/doi/10.1145/3725333). 2. **Intrinsics**. Write the algorithm using explicit [intrinsics](https://en.wikipedia.org/wiki/Intrinsic_function): special functions that compilers map directly into CPU instructions. These are platform dependent, but offer full control. ##### General algorithm [\#](/blog/qbit-vector-search#general-algorithm)

SIMD untransposition is too complex for the compiler to auto\-vectorise, so we’ve taken the second route and will walk you through it. Let’s first look at the idea behind the algorithm, and then see how it fits into the vectorized world.

![Diagram 8.jpg](/uploads/Diagram_8_fa2abe95fa.jpg)
![Diagram 9.jpg](/uploads/Diagram_9_544ae9ea68.jpg)
![Diagram 10.jpg](/uploads/Diagram_10_874d6bf97d.jpg)
![Diagram 11.jpg](/uploads/Diagram_11_e0fcfb28e9.jpg)
We loop through all `FixedString` columns of the QBit (64 of them for `Float64`). Within each column, we iterate over every byte of the `FixedString`, and within each byte, over every bit.

If a bit is **0**, we apply a zero mask to the destination at the corresponding position. If a bit is **1**, we apply a mask that depends on its position within the byte. For example, if we are processing the first bit, the mask is `10000000`; for the second bit, it becomes `01000000`, and so on. The operation we apply is a **logical OR**, merging the bit from the source into the destination byte.

##### Vectorized algorithm [\#](/blog/qbit-vector-search#vectorized-algorithm)

Let’s now look at the second iteration (steps 3 and 4 from above) using **AVX\-512**, an instruction set that’s common across modern CPUs. In this example, we’re unpacking the second `FixedString(1)` group and each bit here contributes to the *second* *bit* of eight resulting `Float64` values.

![Diagram 12.jpg](/uploads/Diagram_12_80c9d0b961.jpg)
When dealing with SIMD, it’s easier to think in *lanes*. AVX\-512 operates on 512\-bit registers, which correspond to eight 64\-bit lanes. Let’s map our fixed strings across those lanes to visualise the data layout.

![Diagram 13.jpg](/uploads/Diagram_13_b2583d8ae5.jpg)
Since we’re unpacking the **second** bit of each `Float64`, the bitmask now has its second bit set.  

We apply that mask across the lanes.

![Diagram 14.jpg](/uploads/Diagram_14_1e9ddccd54.jpg)
The destination (`dst`) already contains results from the previous iteration. We are working on merging in the second bit as well.
