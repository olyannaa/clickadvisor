# CPU Dispatch in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# CPU Dispatch in ClickHouse

![maksim.png](/_next/image?url=%2Fuploads%2Fmaksim_642330ee4f.png&w=96&q=75)[Maksim Kita](/authors/maksim-kita)Oct 3, 2023 · 15 minutes read## Overview [\#](/blog/cpu-dispatch-in-clickhouse#overview)


In this post, I will describe how vectorization works, what CPU dispatch is, how to find places for CPU dispatch optimizations and how we use CPU dispatch in ClickHouse.


First, let’s describe our problem. Hardware vendors constantly add new instructions to the instruction set of modern CPUs. And we often want to use the latest instructions for optimizations, and the most important are [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instructions. But the main issue with this is the compatibility. For example, if your program is compiled with [AVX2](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#Advanced_Vector_Extensions_2) instruction set, and your CPU supports only [SSE4\.2](https://en.wikipedia.org/wiki/SSE4#SSE4.2), then if it runs such a program, you will get an illegal instruction signal ([SIGILL](https://en.wikipedia.org/wiki/Signal_(IPC)#SIGILL)).


Also, an important thing to note is that data structures and algorithms can be specifically designed around SIMD instructions, for example, modern [integer compression codecs](https://onlinelibrary.wiley.com/doi/10.1002/spe.2203), or ported to such instructions later on, for example, [JSON parsing](https://arxiv.org/pdf/1902.08318.pdf).


To improve performance while retaining compatibility with older hardware, parts of your code can be compiled for different instruction sets, and then at runtime the program can dispatch execution to the most performant variant.


For any examples in this post I will use the clang\-15 compiler.


## Vectorization basics [\#](/blog/cpu-dispatch-in-clickhouse#vectorization-basics)


Vectorization is an optimization where your data is processed using vector operations instead of scalar operations. Modern CPUs have specific instructions that allow you to process your data in vectors using [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instructions. Such optimizations can be performed manually, or compilers can perform [automatic vectorization](https://en.wikipedia.org/wiki/Automatic_vectorization).


Let’s consider such code example:



```
void plus(int64_t * __restrict a, int64_t * __restrict b, int64_t * __restrict c, size_t size)
{
   for (size_t i = 0; i < size; ++i) {
       c[i] = b[i] + a[i];
   }
}

```

We have a plus function that takes 3 pointers to `a`, `b` and `c` arrays and size of these arrays. This function computes the sum of a and b array elements and writes it into array c.


If we compile this code without loop unrolling by specifying the option `fno-unroll-loops`, and with AVX2 support specifying via the option `-mavx2`, the following assembly will be generated:



```
$ /usr/bin/clang++-15 -mavx2 -fno-unroll-loops -O3 -S vectorization_example.cpp

```


```
# %bb.0:
	testq	%rcx, %rcx
	je	.LBB0_7
# %bb.1:
	cmpq	$4, %rcx
	jae	.LBB0_3
# %bb.2:
	xorl	%r8d, %r8d
	jmp	.LBB0_6
.LBB0_3:
	movq	%rcx, %r8
	andq	$-4, %r8
	xorl	%eax, %eax
	.p2align	4, 0x90
.LBB0_4:                                # =>This Inner Loop Header: Depth=1
	vmovdqu	(%rdi,%rax,8), %ymm0
	vpaddq	(%rsi,%rax,8), %ymm0, %ymm0
	vmovdqu	%ymm0, (%rdx,%rax,8)
	addq	$4, %rax
	cmpq	%rax, %r8
	jne	.LBB0_4
# %bb.5:
	cmpq	%rcx, %r8
	je	.LBB0_7
	.p2align	4, 0x90
.LBB0_6:                                # =>This Inner Loop Header: Depth=1
	movq	(%rdi,%r8,8), %rax
	addq	(%rsi,%r8,8), %rax
	movq	%rax, (%rdx,%r8,8)
	incq	%r8
	cmpq	%r8, %rcx
	jne	.LBB0_6
.LBB0_7:
	vzeroupper
	retq

```

In the final assembly, there are two loops. The vectorized loop that processes 4 elements at a time:



```
.LBB0_4:                                # =>This Inner Loop Header: Depth=1
	vmovdqu	(%rdi,%rax,8), %ymm0
	vpaddq	(%rsi,%rax,8), %ymm0, %ymm0
	vmovdqu	%ymm0, (%rdx,%rax,8)
	addq	$4, %rax
	cmpq	%rax, %r8
	jne	.LBB0_4

```

And the Scalar loop:



```
.LBB0_6:                                # =>This Inner Loop Header: Depth=1
	movq	(%rdi,%r8,8), %rax
	addq	(%rsi,%r8,8), %rax
	movq	%rax, (%rdx,%r8,8)
	incq	%r8
	cmpq	%r8, %rcx
	jne	.LBB0_6

```

At the beginning of the functions assembly, there is a check depending on the arrays size which determines which loop is chosen:



```
# %bb.1:
	cmpq	$4, %rcx
	jae	.LBB0_3
# %bb.2:
	xorl	%r8d, %r8d
	jmp	.LBB0_6

```

Additionally, an important thing to note is `vzeroupper` instruction. The compiler inserts this to avoid the penalty of mixing SSE and VEX AVX instructions. You can read more about it in [Agner Fog Optimizing subroutines in assembly language: An optimization guide for x86 platforms. 13\.2 Mixing VEX and SSE code](https://www.agner.org/optimize/).


Another important thing to note is the \_\_restrict keyword on the input array pointers. It [tells the compiler](https://en.wikipedia.org/wiki/Restrict) that the function arguments do not alias each other. This means in particular that they do not point to overlapping memory regions. If \_\_restrict is not specified, the compiler will either not vectorize the loop at all or vectorize it only after doing a costly [runtime check](https://llvm.org/docs/Vectorizers.html#runtime-checks-of-pointers) at the beginning of the function to make sure that the arrays do indeed not overlap.


Additionally, if we compile this example without fno\-unroll\-loops and look at the generated loop, we will see that the compiler unrolled the vectorized loop, which now processes 16 elements at a time.



```
.LBB0_4:                                # =>This Inner Loop Header: Depth=1
	vmovdqu	(%rdi,%rax,8), %ymm0
	vmovdqu	32(%rdi,%rax,8), %ymm1
	vmovdqu	64(%rdi,%rax,8), %ymm2
	vmovdqu	96(%rdi,%rax,8), %ymm3
	vpaddq	(%rsi,%rax,8), %ymm0, %ymm0
	vpaddq	32(%rsi,%rax,8), %ymm1, %ymm1
	vpaddq	64(%rsi,%rax,8), %ymm2, %ymm2
	vpaddq	96(%rsi,%rax,8), %ymm3, %ymm3
	vmovdqu	%ymm0, (%rdx,%rax,8)
	vmovdqu	%ymm1, 32(%rdx,%rax,8)
	vmovdqu	%ymm2, 64(%rdx,%rax,8)
	vmovdqu	%ymm3, 96(%rdx,%rax,8)
	addq	$16, %rax
	cmpq	%rax, %r8
	jne	.LBB0_4

```

There is a very useful tool that can help you identify places where the compiler does or does not perform vectorization to avoid assembly checking. You can add `-Rpass=loop-vectorize`, `-Rpass-missed=loop-vectorize` and `-Rpass-analysis=loop-vectorize` options to clang. There are similar [options](https://www.gnu.org/software/gcc/projects/tree-ssa/vectorization.html#using) for gcc.


If we compile our example with these options, there will be the following output:



```
$ /usr/bin/clang++-15 -mavx2 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize -O3

vectorization_example.cpp:7:5: remark: vectorized loop (vectorization width: 4, interleaved count: 4) [-Rpass=loop-vectorize]
    for (size_t i = 0; i < size; ++i) {

```

Now let’s consider another example:



```
class SumFunction
{
public:
    void sumIf(int64_t * values, int8_t * filter, size_t size);

    int64_t sum = 0;
};

void SumFunction::sumIf(int64_t * values, int8_t * filter, size_t size)
{
    for (size_t i = 0; i < size; ++i) {
        sum += filter[i] ? 0 : values[i];
    }
}

```


```
/usr/bin/clang++-15 -mavx2 -O3 -Rpass-analysis=loop-vectorize -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -c vectorization_example.cpp

...

vectorization_example.cpp:28:9: remark: loop not vectorized [-Rpass-missed=loop-vectorize]
        for (size_t i = 0; i < size; ++i) {

```

In case the compiler cannot perform vectorization. There are two possible scenarios:


1. You can try to modify your code, so it can be vectorized. In some complex scenarios, you may need to redesign your data representation. I highly encourage you to check the [LLVM documentation](https://llvm.org/docs/Vectorizers.html) and [gcc documentation](https://www.gnu.org/software/gcc/projects/tree-ssa/vectorization.html) that can help you understand in which cases auto\-vectorization can or cannot be performed.
2. You can vectorize the loop manually using [intrinsics](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html). This option is less preferred because of the additional maintenance.


To fix the issue in our example, we need to make a local sum inside the function:



```
class SumFunction
{
public:
    void sumIf(int64_t * values, int8_t * filter, size_t size);

    int64_t sum = 0;
};

void SumFunction::sumIf(int64_t * values, int8_t * filter, size_t size)
{
    int64_t local_sum = 0;

    for (size_t i = 0; i < size; ++i) {
        local_sum += filter[i] ? 0 : values[i];
    }

    sum += local_sum;
}

```

Such code example is vectorized by the compiler:



```
/usr/bin/clang++-15 -mavx2 -O3 -Rpass-analysis=loop-vectorize -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -c vectorization_example.cpp

vectorization_example.cpp:31:5: remark: vectorized loop (vectorization width: 4, interleaved count: 4) [-Rpass=loop-vectorize]
    for (size_t i = 0; i < size; ++i) {

```

In the resulting assembly vectorized loop looks like this:



```
.LBB0_5:                                # =>This Inner Loop Header: Depth=1
	vmovd	(%rdx,%rax), %xmm5              # xmm5 = mem[0],zero,zero,zero
	vmovd	4(%rdx,%rax), %xmm6             # xmm6 = mem[0],zero,zero,zero
	vmovd	8(%rdx,%rax), %xmm7             # xmm7 = mem[0],zero,zero,zero
	vmovd	12(%rdx,%rax), %xmm1            # xmm1 = mem[0],zero,zero,zero
	vpcmpeqb	%xmm5, %xmm8, %xmm5
	vpmovsxbq	%xmm5, %ymm5
	vpcmpeqb	%xmm6, %xmm8, %xmm6
	vpmovsxbq	%xmm6, %ymm6
	vpcmpeqb	%xmm7, %xmm8, %xmm7
	vpmovsxbq	%xmm7, %ymm7
	vpcmpeqb	%xmm1, %xmm8, %xmm1
	vpmaskmovq	-96(%r8,%rax,8), %ymm5, %ymm5
	vpmovsxbq	%xmm1, %ymm1
	vpmaskmovq	-64(%r8,%rax,8), %ymm6, %ymm6
	vpaddq	%ymm0, %ymm5, %ymm0
	vpmaskmovq	-32(%r8,%rax,8), %ymm7, %ymm5
	vpaddq	%ymm2, %ymm6, %ymm2
	vpmaskmovq	(%r8,%rax,8), %ymm1, %ymm1
	vpaddq	%ymm3, %ymm5, %ymm3
	vpaddq	%ymm4, %ymm1, %ymm4
	addq	$16, %rax
	cmpq	%rax, %r9
	jne	.LBB0_5

```

## CPU Dispatch basics [\#](/blog/cpu-dispatch-in-clickhouse#cpu-dispatch-basics)


CPU dispatch is a technique when there are multiple compiled versions of your code for different CPU features, and in runtime, your program detects which CPU features your machine has and uses the most performant version in runtime. The most important instruction sets you want to check are SSE4\.2, AVX, AVX2, and AVX\-512\.


To implement CPU dispatch, first, we need to use the [CPUID](https://en.wikipedia.org/wiki/CPUID) instruction to check if particular features are supported for the current CPU.


You can call the `cpuid` instruction using inline assembly or using a cpuid.h header where these functions are defined:



```
/* x86-64 uses %rbx as the base register, so preserve it. */
#define __cpuid(__leaf, __eax, __ebx, __ecx, __edx) \
   __asm("  xchgq  %%rbx,%q1\n" \
         "  cpuid\n" \
         "  xchgq  %%rbx,%q1" \
       : "=a"(__eax), "=r" (__ebx), "=c"(__ecx), "=d"(__edx) \
       : "0"(__leaf))

#define __cpuid_count(__leaf, __count, __eax, __ebx, __ecx, __edx) \
   __asm("  xchgq  %%rbx,%q1\n" \
         "  cpuid\n" \
         "  xchgq  %%rbx,%q1" \
       : "=a"(__eax), "=r" (__ebx), "=c"(__ecx), "=d"(__edx) \
       : "0"(__leaf), "2"(__count))
#endif

```

Next, to check if some CPU feature is supported, you need to check [Intel Software Optimization Reference Manual Chapter 5](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) manual for specific instructions. For example, for SSE4\.2:



```
bool hasSSE42()
{
    uint32_t eax = 0;
    uint32_t ebx = 0;
    uint32_t ecx = 0;
    uint32_t edx = 0;

    __cpuid(0x1, eax, ebx, ecx, edx);

    return (ecx >> 20) & 1ul;
}

```

Now we need to compile our function with different instructions. In `clang`, there is [target](https://clang.llvm.org/docs/AttributeReference.html#target) attribute that can do exactly that. In `gcc`, there is the same [attribute](https://gcc.gnu.org/onlinedocs/gcc-12.2.0/gcc/Function-Multiversioning.html#Function-Multiversioning). For example:



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

In this example, we created a plus function that dispatches to a concrete implementation based on the available instruction set. Such a CPU dispatch method is also called dispatch on each call. There are other methods that you can read about in [Agner Fog Optimizing software in C\+\+: An optimization guide for Windows, Linux and Mac platforms. 13\.1 CPU dispatch strategies](https://www.agner.org/optimize/).


Dispatch on each call is the most flexible method because it will allow you to work with template functions and class member functions, or choose an implementation based on some statistics collected in runtime. The only downside is branching, although this overhead is negligible if your function performs a lot of work.


## CPU Dispatch Optimization Places [\#](/blog/cpu-dispatch-in-clickhouse#cpu-dispatch-optimization-places)


Now how to find places where SIMD optimizations can be applied?


1. If you know what loops are hot in your program, you can try to apply CPU dispatch for them.
2. If you have performance tests, you can compile your program with AVX, AVX2, AVX\-512 and compare performance reports to figure out which places can be optimized in your program using CPU dispatch.


This technique with performance tests can be applied not only to CPU dispatch but to many other useful optimizations. The main idea is to compile your code with different configurations (compilers, compiler options, libraries, allocators), and if there is a performance improvement in some places you can manually optimize them. For example:


1. Try different allocators and different libraries.
2. Try different compiler options (loop unrolling, inline threshold).
3. Enable AVX/AVX2/AVX\-512 for build.


## CPU Dispatch in ClickHouse [\#](/blog/cpu-dispatch-in-clickhouse#cpu-dispatch-in-clickhouse)



> We would like to recognize the efforts of Dmitriy Kovalkov who added the [CPU dispatching framework to ClickHouse](https://github.com/ClickHouse/ClickHouse/pull/10058). It served as a basis for the subsequent work described in this article.


First, I want to show how we designed our dispatch framework in ClickHouse.



```
enum class TargetArch : UInt32
{
    Default  = 0,         /// Without any additional compiler options.
    SSE42    = (1 << 0),  /// SSE4.2
    AVX      = (1 << 1),
    AVX2     = (1 << 2),
    AVX512F  = (1 << 3),
    AVX512BW    = (1 << 4),
    AVX512VBMI  = (1 << 5),
    AVX512VBMI2 = (1 << 6),
};

/// Runtime detection.
bool isArchSupported(TargetArch arch);

```

We define an enum `TargetArch` for the target architecture, and inside the `isArchSupported` function we use CPUID instruction set checks that we have already discussed.
Then we define a bunch of `BEGIN_INSTRUCTION_SET_SPECIFIC_CODE` sections that apply a target attribute to the whole code block.


For example, for clang:



```
#   define BEGIN_AVX512F_SPECIFIC_CODE \
_Pragma("clang attribute push(__attribute__((target(\"sse,sse2,sse3,ssse3,sse4,\
    popcnt,avx,avx2, avx512f\"))), apply_to=function)")
\
#   define BEGIN_AVX2_SPECIFIC_CODE \
_Pragma("clang attribute push(__attribute__((target(\"sse,sse2,sse3,ssse3,sse4,\
    popcnt, avx,avx2\"))), apply_to=function)") \
\
#   define END_TARGET_SPECIFIC_CODE \
_Pragma("clang attribute pop")

```

Then for each instruction set, we define a separate namespace `TargetSpecific::INSTRUCTION_SET`. Examples for AVX2 and AVX512:



```
#define DECLARE_AVX2_SPECIFIC_CODE(...) \
BEGIN_AVX2_SPECIFIC_CODE \
namespace TargetSpecific::AVX2 { \
    DUMMY_FUNCTION_DEFINITION \
    using namespace DB::TargetSpecific::AVX2; \
    __VA_ARGS__ \
} \
END_TARGET_SPECIFIC_CODE

#define DECLARE_AVX512F_SPECIFIC_CODE(...) \
BEGIN_AVX512F_SPECIFIC_CODE \
namespace TargetSpecific::AVX512F { \
    DUMMY_FUNCTION_DEFINITION \
    using namespace DB::TargetSpecific::AVX512F; \
    __VA_ARGS__ \
} \
END_TARGET_SPECIFIC_CODE

```

It can be used like this:



```
DECLARE_DEFAULT_CODE (
    int funcImpl() {
        return 1;
    }
) // DECLARE_DEFAULT_CODE

DECLARE_AVX2_SPECIFIC_CODE (
    int funcImpl() {
        return 2;
    }
) // DECLARE_AVX2_SPECIFIC_CODE

/// Dispatcher function
int dispatchFunc() {
#if USE_MULTITARGET_CODE
    if (isArchSupported(TargetArch::AVX2))
        return TargetSpecific::AVX2::funcImpl();
#endif
    return TargetSpecific::Default::funcImpl();
}

```

The examples above work well with standalone functions, but when we have class member functions, they do not work because these cannot be wrapped into the namespace. For such cases, we have another bunch of macros. We need to insert a specific attribute before the class member function name and generate functions with different names, ideally with suffixes like SSE42, AVX2, AVX512\.
We can split a function into a header and body using the `MULTITARGET_FUNCTION_HEADER` and `MULTITARGET_FUNCTION_BODY` macros. Specific attributes are then inserted before the function name. For example, for AVX\-512 (BW), AVX\-512 (F), AVX2 and SSE4\.2 it can look like this:



```
/// Function header
#define MULTITARGET_FUNCTION_HEADER(...) __VA_ARGS__

/// Function body
#define MULTITARGET_FUNCTION_BODY(...) __VA_ARGS__

#define MULTITARGET_FUNCTION_AVX512BW_AVX512F_AVX2_SSE42(FUNCTION_HEADER, name, FUNCTION_BODY) \
    FUNCTION_HEADER \
    \
    AVX512BW_FUNCTION_SPECIFIC_ATTRIBUTE \
    name##AVX512BW \
    FUNCTION_BODY \
    \
    FUNCTION_HEADER \
    \
    AVX512_FUNCTION_SPECIFIC_ATTRIBUTE \
    name##AVX512 \
    FUNCTION_BODY \
    \
    FUNCTION_HEADER \
    \
    AVX2_FUNCTION_SPECIFIC_ATTRIBUTE \
    name##AVX2 \
    FUNCTION_BODY \
    \
    FUNCTION_HEADER \
    \
    SSE42_FUNCTION_SPECIFIC_ATTRIBUTE \
    name##SSE42 \
    FUNCTION_BODY \
    \
    FUNCTION_HEADER \
    \
    name \
    FUNCTION_BODY \

```

We use CPU dispatch in computationally intensive places, for example, in hashing, geometry functions, string processing functions, random numbers generation functions, unary functions, and aggregate functions.
For example, let’s see how we use CPU dispatch in aggregate functions. In ClickHouse, if there is `GROUP BY` without keys, for example `SELECT sum(value), avg(value) FROM test_table`, the aggregate functions process data directly in a batch. For the `sum` function, there is the following implementation:



```
template <typename Value>
void NO_INLINE addManyImpl(const Value * __restrict ptr, size_t start, size_t end)
{
    ptr += start;
    size_t count = end - start;
    const auto * end_ptr = ptr + count;

    /// Loop
    T local_sum{};
    while (ptr < end_ptr)
    {
        Impl::add(local_sum, *ptr);
        ++ptr;
    }
    Impl::add(sum, local_sum);
}

```

After we wrap this loop into our dispatch framework, the function code will look like this:



```
MULTITARGET_FUNCTION_AVX512BW_AVX512F_AVX2_SSE42(
MULTITARGET_FUNCTION_HEADER(
template <typename Value>
void NO_SANITIZE_UNDEFINED NO_INLINE
), addManyImpl,
MULTITARGET_FUNCTION_BODY((const Value * __restrict ptr, size_t start, size_t end)
{
    ptr += start;
    size_t count = end - start;
    const auto * end_ptr = ptr + count;

    /// Loop
    T local_sum{};
    while (ptr &lt end_ptr)
    {
        Impl::add(local_sum, *ptr);
        ++ptr;
    }
    Impl::add(sum, local_sum);
}))

```

We can now dispatch to the right implementation based on the fastest available CPU instruction set:



```
template <typename Value>
void NO_INLINE addMany(const Value * __restrict ptr, size_t start, size_t end)
{
#if USE_MULTITARGET_CODE
 if (isArchSupported(TargetArch::AVX512BW))
    {
        addManyImplAVX512BW(ptr, start, end);
        return;
    } 
    else if (isArchSupported(TargetArch::AVX512F))
    {
        addManyImplAVX512F(ptr, start, end);
        return;
    }
    else if (isArchSupported(TargetArch::AVX2))
    {
        addManyImplAVX2(ptr, start, end);
        return;
    }
    else if (isArchSupported(TargetArch::SSE42))
    {
        addManyImplSSE42(ptr, start, end);
        return;
    }
#endif

    addManyImpl(ptr, start, end);
}

```

Here is a small part of the performance report after this optimization was applied:




| Query | Old (s) | New (s) | Ratio of speedup(\-) or slowdown(\+) | Relative difference (new \- old) / old |
| --- | --- | --- | --- | --- |
| SELECT sum(toNullable(toUInt8(number))) FROM numbers(100000000\) | 0\.110 | 0\.077 | \-1\.428x | \-0\.300 |
| SELECT sum(number) FROM numbers(100000000\) | 0\.044 | 0\.035 | \-1\.228x | \-0\.185 |
| SELECT sumOrNull(number) FROM numbers(100000000\) | 0\.044 | 0\.036 | \-1\.226x | \-0\.183 |
| SELECT avg(number) FROM numbers(100000000\) | 0\.416 | 0\.341 | \-1\.219x | \-0\.180 |


In general, such optimization for sum and avg aggregate functions improves performance 1\.2\-1\.6 times. Similar optimizations can be applied to other aggregate functions as well.
Now let’s take a look at a CPU dispatch optimization in unary functions:



```
template <typename A, typename Op>
struct UnaryOperationImpl
{
    using ResultType = typename Op::ResultType;
    using ColVecA = ColumnVectorOrDecimal<A>;
    using ColVecC = ColumnVectorOrDecimal<ResultType>
    using ArrayA = typename ColVecA::Container;
    using ArrayC = typename ColVecC::Container;

    static void vector(const ArrayA & a, ArrayC & c)
    {
        /// Loop Op::apply is template for operation
        size_t size = a.size();
        for (size_t i = 0; i < size; ++i)
            c[i] = Op::apply(a[i]);
    }

    static void constant(A a, ResultType & c)
    {
        c = Op::apply(a);
    }
};

```

In the example, there is a loop that applies some template operation using `Op::apply` on elements of array `a` and writes the result into array `c`. After we wrap this loop into our dispatch framework, the loop code will look like this:



```
MULTITARGET_FUNCTION_WRAPPER_AVX2_SSE42(
MULTITARGET_FH(static void NO_INLINE),
vectorImpl,
MULTITARGET_FB((const ArrayA & a, ArrayC & c) /// NOLINT
{
    /// Loop Op::apply is template for operation
    size_t size = a.size();
    for (size_t i = 0; i < size; ++i)
        c[i] = Op::apply(a[i]);
}))

```

Now we need to dispatch to the appropriate function based on the currently available CPU instruction set:



```
static void NO_INLINE vector(const ArrayA & a, ArrayC & c)
{
#if USE_MULTITARGET_CODE
    if (isArchSupported(TargetArch::AVX2))
    {
        vectorImplAVX2(a, c);
        return;
    }
    else if (isArchSupported(TargetArch::SSE42))
    {
        vectorImplSSE42(a, c);
        return;
    }
#endif

    vectorImpl(a, c);
}

```

Here is a small part of the performance report after this optimization was applied:




| Query | Old (s) | New (s) | Ratio of speedup(\-) or slowdown(\+) | Relative difference (new \- old) / old |
| --- | --- | --- | --- | --- |
| SELECT roundDuration(toInt32(number))) FROM numbers(100000000\) | 1\.632 | 0\.229 | \-7\.119x | \-0\.860 |
| SELECT intExp2(toInt32(number)) FROM numbers(100000000\) | 0\.148 | 0\.105 | \-1\.413x | \-0\.293 |
| SELECT roundToExp2(toUInt8(number)) FROM numbers(100000000\) | 0\.144 | 0\.102 | \-1\.41x | \-0\.291 |


In general, such optimization for unary functions improves performance 1\.15\-2 times. For some specific functions like `roundDuration` such optimizations improved performance 2\-7 times.


## Summary [\#](/blog/cpu-dispatch-in-clickhouse#summary)


The compiler can vectorize even complex loops using SIMD instructions. Additionally, you can vectorize your code manually or design SIMD\-oriented algorithms. But the biggest problem is that if you want to use modern instruction sets, it can decrease your program or library portability. Runtime CPU dispatching can help you eliminate this problem, with the cost of compiling parts of your code multiple times for different architectures.
You can find places to improve performance using performance tests and compiling your code with different configurations. For CPU dispatch optimizations, you can compile your code with AVX, AVX2, AVX512 and manually apply CPU dispatch in places where there are performance improvements.
In ClickHouse, we designed a framework specifically for such optimizations and have improved performance in a lot of places as a result.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
