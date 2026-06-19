---
source: blog
url: https://en.wikipedia.org/wiki/Single_instruction,_multiple_data
topic: cpu-dispatch-in-clickhouse
ch_version_introduced: '10.1002'
last_updated: '2026-06-12'
chunk_index: 6
total_chunks_in_doc: 12
---

return (ecx >> 20) & 1ul; } ``` Now we need to compile our function with different instructions. In `clang`, there is [target](https://clang.llvm.org/docs/AttributeReference.html#target) attribute that can do exactly that. In `gcc`, there is the same [attribute](https://gcc.gnu.org/onlinedocs/gcc-12.2.0/gcc/Function-Multiversioning.html#Function-Multiversioning). For example:

```
void plusDefault(int64_t * __restrict a, int64_t * __restrict b, int64_t * __restrict c, size_t size)
{
    for (size_t i = 0; i < size; ++i) {
        c[i] = a[i] + b[i];
    }
}

__attribute__((target("sse,sse2,sse3,ssse3,sse4,avx,avx2")))
void plusAVX2(int64_t * __restrict a, int64_t * __restrict b, int64_t * __restrict c, size_t size)
{
    for (size_t i = 0; i < size; ++i) {
        c[i] = a[i] + b[i];
    }
}

__attribute__((target("sse,sse2,sse3,ssse3,sse4,avx,avx2,avx512f")))
void plusAVX512(int64_t * __restrict a, int64_t * __restrict b, int64_t * __restrict c, size_t size)
{
    for (size_t i = 0; i < size; ++i) {
        c[i] = a[i] + b[i];
    }
}

```

In this example, we compile our plus function additionally for AVX2 and AVX\-512\. In the final assembly, we can check that the compiler uses AVX2 to vectorize the loop of the `plusAVX2` function:

```
...

.globl	_Z8plusAVX2PlS_S_m              # -- Begin function _Z8plusAVX2PlS_S_m

...

.LBB4_4:                                # =>This Inner Loop Header: Depth=1
	vmovdqu	(%rsi,%rax,8), %ymm0
	vmovdqu	32(%rsi,%rax,8), %ymm1
	vmovdqu	64(%rsi,%rax,8), %ymm2
	vmovdqu	96(%rsi,%rax,8), %ymm3
	vpaddq	(%rdi,%rax,8), %ymm0, %ymm0
	vpaddq	32(%rdi,%rax,8), %ymm1, %ymm1
	vpaddq	64(%rdi,%rax,8), %ymm2, %ymm2
	vpaddq	96(%rdi,%rax,8), %ymm3, %ymm3
	vmovdqu	%ymm0, (%rdx,%rax,8)
	vmovdqu	%ymm1, 32(%rdx,%rax,8)
	vmovdqu	%ymm2, 64(%rdx,%rax,8)
	vmovdqu	%ymm3, 96(%rdx,%rax,8)
	addq	$16, %rax
	cmpq	%rax, %r8
	jne	.LBB4_4

...

```

and AVX\-512 for vectorized loop of `plusAVX512`:

```
...

.globl	_Z10plusAVX512PlS_S_m    # -- Begin function _Z10plusAVX512PlS_S_m

...

.LBB5_4:    # =>This Inner Loop Header: Depth=1
	vmovdqu64	(%rsi,%rax,8), %zmm0
	vmovdqu64	64(%rsi,%rax,8), %zmm1
	vmovdqu64	128(%rsi,%rax,8), %zmm2
	vmovdqu64	192(%rsi,%rax,8), %zmm3
	vpaddq	(%rdi,%rax,8), %zmm0, %zmm0
	vpaddq	64(%rdi,%rax,8), %zmm1, %zmm1
	vpaddq	128(%rdi,%rax,8), %zmm2, %zmm2
	vpaddq	192(%rdi,%rax,8), %zmm3, %zmm3
	vmovdqu64	%zmm0, (%rdx,%rax,8)
	vmovdqu64	%zmm1, 64(%rdx,%rax,8)
	vmovdqu64	%zmm2, 128(%rdx,%rax,8)
	vmovdqu64	%zmm3, 192(%rdx,%rax,8)
	addq	$32, %rax
	cmpq	%rax, %r8
	jne	.LBB5_4

...

```

Now we have everything we need to perform a CPU dispatch:

```
void plus(int64_t * __restrict a, int64_t * __restrict b, int64_t * __restrict c, size_t size)
{
    if (hasAVX512()) {
        plusAVX512(a, b, c, size);
    } else if (hasAVX2()) {
        plusAVX2(a, b, c, size);
    } else {
        plusDefault(a, b, c, size);
    }
}

```
