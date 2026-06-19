# JIT in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# JIT in ClickHouse

![maksim.png](/_next/image?url=%2Fuploads%2Fmaksim_642330ee4f.png&w=96&q=75)[Maksim Kita](/authors/maksim-kita)Nov 23, 2022 · 30 minutes read![just_in_time.jpg](/uploads/large_just_in_time_d9c935fa41.jpg)
*This blog post was originally posted on [Maksim's personal blog](https://maksimkita.com/), which we recommend for those interested in the low\-level details of Performance Engineering, Query Analysis and Planning, JIT Compilation, System Programming and Distributed Systems.*


## Overview [\#](/blog/clickhouse-just-in-time-compiler-jit#overview)


In this post, I will describe what JIT compilation is, how LLVM infrastructure can be used for JIT compilation, and how JIT compilation works in ClickHouse.


Most of this post is a summary of talks that I give on C\+\+ Russia 2021 “JIT in ClickHouse”, HighLoad 2022 “JIT compilation of queries in ClickHouse”, C\+\+ Russia 2022 “ClickHouse performance optimization practices”, and there are also additional examples and things that I have not covered in these talks.


## JIT basics [\#](/blog/clickhouse-just-in-time-compiler-jit#jit-basics)


First, let’s start with what JIT compilation is. [JIT](https://en.wikipedia.org/wiki/Just-in-time_compilation) \- Just\-in\-time compilation. The main idea is to generate machine code and execute it in runtime. Examples of such systems are JVM Hotspot and V8\. Most database systems support JIT compilation.


To better understand how JIT compilation works, we can start from the bottom up \- make JIT compilation with our bare hands.


Consider such code example:



```
int64_t sum(int64_t value_1, int64_t value_2)
{
    return value_1 + value_2;
}

int main(int argc, char ** argv)
{
    printf("Sum %ld\n", sum(1, 2));
    return 0;
}

```

We have a `sum` function that takes two integer values, computes their sum, and returns it. In the `main` function, we print the result of the `sum` function execution with constants 1 and 2\.


If we compile this example with gcc and explore binary using [objdump](https://en.wikipedia.org/wiki/Objdump), we can extract `sum` function assembly.



```
g++ --version
g++ (Ubuntu 10.3.0-1ubuntu1~20.04) 10.3.0

```


```

$ g++ -O2 jit_example.cpp -o jit_example
$ objdump -D jit_example | grep sum -A5

0000000000001180 <_Z3sumll>:
  1180:	f3 0f 1e fa             endbr64
  1184:	48 8d 04 37             lea    (%rdi,%rsi,1),%rax /// %rax = %rdi + %rsi * 1
  1188:	c3                      retq
  1189:	0f 1f 80 00 00 00 00    nopl   0x0(%rax)


```


To understand this assembly, we need to know that on my machine, there is [`System_V_AMD64_ABI` calling convention](https://en.wikipedia.org/wiki/X86_calling_conventions#System_V_AMD64_ABI) where the first two function arguments are passed in `rdi`, `rsi` registers, and function result is stored in `rax` register. In `sum` function body the `endbr64` instruction is used to detect control flow violations, `lea` instruction is used to compute the sum of `rdi` and `rsi` registers and put the result in the `rax` register.


Now let’s look at [ELF (Executable and Linkable format)](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format).


![elf.svg](/uploads/elf_8377a7d54e.svg)
An ELF consists of ELF header, program header, section header, and sections. A program header table describes information about segments and section\-to\-segments mapping that is necessary for the operating system to execute binary (executable point of view). A section header table describes information about sections (linker point of view). More information can be found on [man page](https://man7.org/linux/man-pages/man5/elf.5.html), and in the [linux base specification](https://refspecs.linuxbase.org/elf/gabi4+/ch4.intro.html).


We are interested in the linker point of view. Let’s see which sections using [readelf](https://en.wikipedia.org/wiki/Readelf) are inside the ELF file.



```

$ readelf -S jit_example

There are 31 section headers, starting at offset 0x39a8:

Section Headers:

...

[16] .text             PROGBITS         0000000000001060  00001060
00000000000001a5  0000000000000000  AX       0     0     16
[18] .rodata           PROGBITS         0000000000002000  00002000
000000000000000d  0000000000000000   A       0     0     4
[25] .data             PROGBITS         0000000000004000  00003000
0000000000000010  0000000000000000  WA       0     0     8

...

Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  l (large), p (processor specific)


```


Important things to note here are that the `.text` section has READ \+ EXECUTE permissions, the `.rodata` section has only READ permissions, and the `.data` section has READ \+ WRITE permissions.


If we check the `.rodata` section dump, we can see that linker puts a constant used as the first argument of `printf` function into it.



```
printf("Sum %ld\n", sum(1, 2));

```


```
$ readelf -x .rodata jit_example

Hex dump of section '.rodata':
0x00002000 01000200 53756d20 256c640a 00       ....Sum %ld..

```

We can explicitly check that our `sum` function is in the `.text` section.



```
$ objdump -D jit_example | grep sum -A5

0000000000001180 <_Z3sumll>:
    1180:	f3 0f 1e fa          	endbr64
    1184:	48 8d 04 37          	lea    (%rdi,%rsi,1),%rax
    1188:	c3                   	retq
    1189:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

```


```
$ readelf -x .text jit_example

Hex dump of section '.text':
0x00001060 f30f1efa 4883ec08 ba030000 00bf0100 ....H...........
...
0x00001180 f30f1efa 488d0437 c30f1f80 00000000 ....H..7........
0x00001190 f30f1efa 41574c8d 3d1b2c00 00415649 ....AWL.=.,..AVI
0x000011a0 89d64155 4989f541 544189fc 55488d2d ..AUI..ATA..UH.-
...
0x00001200 f30f1efa c3                         ....

```

Now we have everything we need to do the same thing with our bare hands.



```
1144:   48 8d 04 37             lea    (%rdi,%rsi,1),%rax
1148:   c3                      retq

```


```
int64_t jitSum(int64_t value_1, int64_t value_2)
{
    /// Allocate page with READ + WRITE + EXECUTE permissions
    char * res = static_cast(mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
            MAP_PRIVATE | MAP_ANON, -1, 0));

    size_t instruction = 0;

    /// lea (%rdi, %rsi, 1), %rax => rax = rdi + rsi * 1
    res[instruction++] = 0x48;
    res[instruction++] = 0x8d;
    res[instruction++] = 0x04;
    res[instruction++] = 0x37;

    /// retq
    res[instruction++] = 0xc3;

    using SumFunction = int64_t (*)(int64_t, int64_t);
    SumFunction func = reinterpret_cast<SumFunction>(res);

    return func(value_1, value_2);
}

int main(int argc, char ** argv)
{
    printf("Sum %ld\n", jitSum(1, 2));
    return 0;
}

```

This example is a bit more complex, so let me explain what is going on here.


1. Allocate memory for our code to be executed using `mmap`. We can also use any page\-aligned memory and `mprotect` it.
2. Put encoded instructions directly in memory: `48 8d 04 37` for `lea` and `0xc3` for retq instruction.
3. Cast our page pointer to the function pointer type that we expect. After that function is ready to be executed.


We can verify that it works as expected.



```
$ g++ -O2 jit_example.cpp -o jit_example
$ ./jit_example

$ Sum 3

```

But one question that is not answered yet is how we can interact with our program from JIT code. Consider this example:



```
void test_function()
{
   printf("JIT example\n");
}

void jitTestFuncCall()
{
   /// Allocate page with READ + WRITE + EXECUTE permissions
   char * res = static_cast<char *>(mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
       MAP_PRIVATE | MAP_ANON, -1, 0));

   size_t instruction = 0;

   /// movabs [pointer_to_test_function], %rax
   res[instruction++] = 0x48;
   res[instruction++] = 0xb8;

   ptrdiff_t test_function_raw_ptr = reinterpret_cast<ptrdiff_t>(test_function);
   memcpy(res + instruction, &test_function_raw_ptr, sizeof(ptrdiff_t));
   instruction += sizeof(ptrdiff_t);

   /// callq *%rax
   res[instruction++] = 0xff;
   res[instruction++] = 0xd0;

   /// retq
   res[instruction++] = 0xc3;

   using VoidFunction = void (*)(void);
   VoidFunction func = reinterpret_cast<VoidFunction>(res);
   func();
}

int main(int argc, char ** argv)
{
   jitTestFuncCall();
   return 0;
}

```

In this example, we want to call the `test_function` function from JIT code. We do almost the same stuff as in the previous example, but instead of `lea` instruction encoding, we encode `movabs [pointer_to_test_function], %rax` and `callq *%rax` instructions.


We can verify that it works.



```
$ g++ -O2 jit_example.cpp -o jit_example
$ ./jit_example

$ JIT example

```

All interaction between JIT code and code in our main program is typically done this way, we pass pointers to functions in JIT code and call it from JIT code.


## LLVM infrastructure for JIT compilation [\#](/blog/clickhouse-just-in-time-compiler-jit#llvm-infrastructure-for-jit-compilation)


On a high level for JIT compilation LLVM has the following things:


- Optimizing compiler. Optimization passes can be configured, and you can also vary optimization level based on your specific use cases. For example, you can first compile your code without optimizations and later recompile it with optimizations.
- Dynamic Linker that is used to resolve [relocations](https://en.wikipedia.org/wiki/Relocation_(computing)), allocate necessary code and data sections, and prepare compiled object files for execution.
- LLVM IR (LLVM intermediate language representation).
- A lot of LLVM toolings like IR and assembly printers. Special JIT tooling to support GDB and perf. MCJIT, ORCJIT JIT compilers. In ClickHouse, we do not use them, but you can check out their implementation to understand how things work inside them.


LLVM IR is an intermediate language representation used in LLVM.


- [Static Single Assignment](https://en.wikipedia.org/wiki/Static_single-assignment_form). Each variable is assigned only once.
- Strongly typed. Compilation will fail during the IR verification stage, if you do not get the types right.
- Allows to map high\-level constructions into low\-level representation. LLVM IR has support for modules, functions, and structures.


Let’s see how it looks like:



```
int64_t sum(int64_t value_1, int64_t value_2)
{
    return value_1 + value_2;
}

```


```
/usr/bin/clang++-12 -S -emit-llvm jit_example.cpp

; Function Attrs: noinline nounwind optnone uwtable mustprogress
define dso_local i64 @_Z3sumll(i64 %0, i64 %1) #0 {
  %3 = alloca i64, align 8 /// alloca - allocate memory on stack
  %4 = alloca i64, align 8
  store i64 %0, i64* %3, align 8 /// store - store value in pointer
  store i64 %1, i64* %4, align 8
  %5 = load i64, i64* %3, align 8 /// load - load value from pointer
  %6 = load i64, i64* %4, align 8
  %7 = add nsw i64 %5, %6 /// nsw - No Signed Wrap
  ret i64 %7
}

```

We will not use a lot of LLVM IR later in this post, but I highly encourage you to check the LLVM IR documentation.


Now let’s take a look at LLVM high\-level components.


- TargetMachine \- machine target specific information. Allowed CPU instructions, data layout, etc.
- LLVMContext \- context for LLVM global data.
- IRBuilder \- builder for LLVM IR.
- Value \- base class for all computed values (local variables, global variables, function arguments, constants).
- Function \- function container for BasicBlocks.
- BasicBlock \- container for LLVM IR instructions executed sequentially until termination instruction (return, jump).
- Module \- container for IR objects, including functions and global variables. It also stores information about target characteristics.
- PassManager \- module pass manager.
- FunctionPassManager \- function pass manager.
- PassManagerBuilder \- builder for module and function optimization passes, used to populate PassManager and FunctionPassManager.
- ObjectFile \- object file.
- RuntimeDyld \- dynamic linker, takes object file and starts a dynamic linking process, allocates and fills code and data sections, resolves [relocations](https://en.wikipedia.org/wiki/Relocation_(computing)).
- RTDyldMemoryManager \- dynamic linker memory manager. Allocates necessary code and data sections during linking. Owner of memory allocated during linkage.
- JITSymbolResolver \- resolve external symbols during dynamic linking.


Strategy for JIT code compilation using LLVM high\-level components:


1. Create a Module and fill it with Functions. Apply optimizations using PassManagerBuilder, FunctionPassManager, and PassManager.
2. Setup passes in PassManager to emit an ObjectFile from Module using TargetMachine.
3. Create JITSymbolResolver for resolving external symbols, for example `memset`.
4. Create RTDyldMemoryManager for the RuntimeDyld dynamic linker.
5. Resolve [relocations](https://en.wikipedia.org/wiki/Relocation_(computing)) and create necessary code and data sections for ObjectFile using RuntimeDyld dynamic linker.
6. Get function symbols pointers from compiled code using RuntimeDyld dynamic linker.


Our wrapper interface around JIT compilation looks like this:



```
class CHJIT
{
    struct CompiledModule
    {
        /// Size of compiled module code in bytes
        size_t size;

        /// Module identifier. Should not be changed by client
        uint64_t identifier;

        /// Map of compiled functions. Should not be changed by client
        std::unordered_map<std::string, void *> function_name_to_symbol;
    };

    /// Compile module. Client must fill module with necessary IR code.
    CompiledModule compileModule(std::function<void (llvm::Module &)> compile_function);

    /** Delete compiled module.
      * Pointers to functions from module become invalid after this call.
      */
    void deleteCompiledModule(const CompiledModule & module_info);

    /// Register external symbol for CHJIT instance to use, during linking.
    void registerExternalSymbol(const std::string & symbol_name, void * address);

    /// Total compiled code size for modules that are currently valid.
    inline size_t getCompiledCodeSize() const;
}

```

In the implementation, our wrapper uses the same strategy as described above. Additionally it:


- Stores RTDyldMemoryManager for each compiled module to allow it to be deleted if requested.
- Sets up JITSymbolResolver with common functions that can be generated by compiler memset, memcpy, memcmp.
- Uses a custom allocator for JIT code.
- Provides thread safety.


Now let’s see a small example of how this abstraction is used.



```
auto jit = DB::CHJIT();

auto compiled_sum_module = jit.compileModule([](llvm::Module & module)
{
    llvm::LLVMContext & context = module.getContext();
    llvm::IRBuilder<> b(context);

    llvm::Type * int64_type = b.getInt64Ty();
    std::vector params = {int64_type, int64_type};
    bool is_var_args = false;
    llvm::FunctionType * func_type =
        llvm::FunctionType::get(int64_type, params, is_var_args);

    llvm::Function::LinkageTypes linkage = 
    llvm::Function::ExternalLinkage;
    llvm::Function * function =
        llvm::Function::Create(func_type, linkage, "sum", module);

    /// Get first argument
    llvm::Value * first_argument = function->args().begin();

    /// Get second argument
    llvm::Value * second_argument = function->args().begin() + 1;

    /// Create function entry basic block
    llvm::BasicBlock * entry = 
    llvm::BasicBlock::Create(context, "entry", function);
    b.SetInsertPoint(entry);

    /// Sum arguments
    llvm::Value * sum = b.CreateAdd(first_argument, second_argument);

    /// Return sum result
    b.CreateRet(sum);
});

using SumFunc = int64_t (*)(int64_t, int64_t);
auto sum_func = 
reinterpret_cast(compiled_sum_module.function_name_to_symbol["sum"]);
printf("Sum %ld\n", sum_func(1, 2));

jit.deleteCompiledModule(compiled_sum_module);

```

Here we create our CHJIT wrapper, call the `compileModule` function and add the `sum` LLVM function (which consists of 1 BasicBlock) into the Module using IRBuilder. Such `sum` function is compiled into this IR:



```
define i64 @sum(i64 %0, i64 %1) {
    entry:
    %2 = add i64 %0, %1
    ret i64 %2
}

```

And later into this assembler (If we specify O3 optimization):



```
.text
	.file	"jit0"
	.globl	sum                             # -- Begin function sum
	.p2align	4, 0x90
	.type	sum,@function
sum:                                    # @sum
# %bb.0:                                # %entry
	leaq	(%rdi,%rsi), %rax
	retq
.Lfunc_end0:
	.size	sum, .Lfunc_end0-sum # -- End function

```

An additional thing to note is integration with LLVM. LLVM is compiled without exceptions, and in a lot of places, asserts are used to verify invariants. In release builds, this can be an issue because these asserts are not checked. In our case, the biggest problem was that if your constructed LLVM IR is not well\-formed, LLVM will crash, or compiled code will be broken and potentially could crash in runtime. We solve this with additional testing and AST fuzzing in our CI/CD infrastructure.


## ClickHouse basics [\#](/blog/clickhouse-just-in-time-compiler-jit#clickhouse-basics)


ClickHouse is a column\-oriented DBMS. It has column\-oriented storage and a vectorized query execution engine.


In column\-oriented storage, data is physically stored by columns.


- Only necessary columns are read from the disk during the query.
- Better compression because similar data lies nearly.


Both factors significantly reduce the amount of IO during query execution.


Vectorized query execution engine process data in blocks. Block contains multiple columns with max\_block\_size rows (65505 by default). Each column is stored as a vector of primitive data types or their combination:


- Better utilization for CPU caches and pipelines.
- Data can be processed using SIMD instructions.


The most important component is IColumn:



```
class IColumn
{
    ...

    virtual ~IColumn() = default;

    [[nodiscard]] virtual Ptr filter(const Filter & filt, ssize_t result_size_hint) const = 0;

    [[nodiscard]] virtual Ptr permute(const Permutation & perm, size_t limit) const = 0;

    virtual void insertFrom(const IColumn & src, size_t n);

    virtual void insertRangeFrom(const IColumn & src, size_t start, size_t length) = 0;

    ...
}

```

It declares methods that all concrete column types need to support, for example, `filter` or `permute`. In most of the functions, IColumn is unwrapped to a concrete type. Each column is stored as an array of primitive types or their compositions.


Numeric columns are stored using PaddedPODArray. It is almost the same as `std::vector` with a few differences:


- It uses our allocator that supports `realloc` (for big memory chunks, it is implemented using `mremap`).
- No additional `memset` during resize.
- Padding with 15 bytes at the end. This allows a more efficient implementation of `memcpy` function, where it does not have additional checks for handling tails.


Other columns are implemented as a composition of numeric columns:


- Nullable column contains data column and UInt8 column, where each value represents whether the element is null.
- String column contains UInt8 data column and UInt64 column with offsets.
- Array column contains data column and UInt64 column with offsets.
- Const column contains 1 constant value.


The next important component in our execution engine is IFunction:



```
class IFunction
{
    ...

    virtual ~IFunction() = default;

    virtual ColumnPtr executeImpl(
        const ColumnsWithTypeAndName & arguments,
        const DataTypePtr & result_type,
        size_t input_rows_count) const = 0;

    ...
}

```

There are a lot of specializations for functions:


- Specializations for different types and their combinations.
- Specializations for constant columns.


Function `plus` has:



```
UInt8 UInt16 UInt32 UInt64      UInt8 UInt16 UInt32 UInt64
    Int8 Int16 Int32 Int64  ✕      Int8 Int16 Int32 Int64
            Float32 Float64             Float32 Float64

```

specializations for different types. And in addition, specializations if one of the columns is a constant column. In result 20 x 20 \= 400 specializations for single `plus` function.


Advantages of the current interface:


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



```
EXPLAIN PLAN SELECT value * 2 + 1 FROM test_table
WHERE value > 10 ORDER BY value;

┌─explain──────────────────────────────────────────────────────────┐
│ Expression ((Projection + Before ORDER BY [lifted up part]))     │
│   Sorting (Sorting for ORDER BY)                                 │
│     Expression (Before ORDER BY)                                 │
│       Filter (WHERE)                                             │
│         SettingQuotaAndLimits                                    │
│           ReadFromMergeTree (default.test_table)                 │
└──────────────────────────────────────────────────────────────────┘

```

Explain physical query plan:



```
EXPLAIN PIPELINE SELECT value * 2 + 1 FROM test_table
WHERE value > 10 ORDER BY value;

┌─explain────────────────────────────────────┐
│ (Expression)                               │
│ ExpressionTransform                        │
│   (Sorting)                                │
│   MergingSortedTransform 16 → 1            │
│     MergeSortingTransform × 16             │
│       LimitsCheckingTransform × 16         │
│         PartialSortingTransform × 16       │
│           (Expression)                     │
│           ExpressionTransform × 16         │
│             (Filter)                       │
│             FilterTransform × 16           │
│               (SettingQuotaAndLimits)      │
│                 (ReadFromMergeTree)        │
│                 MergeTreeThread × 16 0 → 1 │
└────────────────────────────────────────────┘

```

## ClickHouse compilation of expressions [\#](/blog/clickhouse-just-in-time-compiler-jit#clickhouse-compilation-of-expressions)


During different steps of SQL query execution, the execution engine needs to compute expressions. For example:



```
EXPLAIN PIPELINE SELECT value * 2 + 1 FROM test_table
WHERE value > 10 ORDER BY value;

┌─explain────────────────────────────────────┐
│ (Expression)                               │
│ ExpressionTransform                        │
│   (Sorting)                                │
│   MergingSortedTransform 16 → 1            │
│     MergeSortingTransform × 16             │
│       LimitsCheckingTransform × 16         │
│         PartialSortingTransform × 16       │
│           (Expression)                     │
│           ExpressionTransform × 16         │
│             (Filter)                       │
│             FilterTransform × 16           │
│               (SettingQuotaAndLimits)      │
│                 (ReadFromMergeTree)        │
│                 MergeTreeThread × 16 0 → 1 │
└────────────────────────────────────────────┘

```

It is necessary for execution engine to evaluate `value > 10`, and `value * 2 + 1` expressions during query execution. In the physical query plan, this step is called `ExpressionTransform`. Expressions are represented as expression [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) that has `input`, `function` and `constant` type of nodes.


Example of `plus(plus(a, multiply(b, c)), 5)` DAG:


![actions_dag.svg](/uploads/actions_dag_dc019485f0.svg)
The main issue with DAG interpretation is that data is moving between functions. Operations are not fused. For example, for such DAG `plus(plus(a, b), c))`, first `plus(a, b)` is performed and the result is stored in a temporary column. Then `plus` with temporary column and column `c` is performed.


To support JIT compilation, support into IFunction interface is added:



```
class IFunction
{
    ...

    bool isCompilable(const DataTypes & arguments) const;

    llvm::Value * compile(
        llvm::IRBuilderBase & builder,
        const DataTypes & arguments_types,
        std::vector<llvm::Value *> arguments) const;

    ...
}

```

If a function can be compiled for specific data types, it must return true in `isCompilable` method. And during the `compile` method call, apply logic using IRBuilder to arguments and return the result.


Currently compilation is supported for:


- Binary operators. Example: `plus`, `minus`, `multiply`, `xor`.
- Unary operators. Example: `abs`.
- Logical functions. Example: `and`, `or`, `not`.
- Conditional functions. Example: `if`, `multiIf`.
- Bit shift functions. Example: `bitShiftLeft`.


JIT expressions compilation algorithm:


1. For each node in DAG compute `children_size`, `compilable_children_size`.
2. Sort nodes in descending order of `compilable_children_size`, to first compile nodes with most children.
3. Check if a node can be compiled using heuristics. Currently, we require a node to contain at least 1 compilable children.
4. Compile the node and its compilable children together into a function. This function takes raw column data pointers and returns expression results.
5. Replace the node in DAG with special `LLVMFunction` node. `LLVMFunction` execute method converts columns into raw data and calls compiled function.


Assume we have such DAG `plus(plus(a, multiply(b, c)), 5)`:


![actions_dag.svg](/uploads/actions_dag_dc019485f0.svg)
After JIT compilation, DAG will look like this:


![actions_dag_after_compilation.svg](/uploads/actions_dag_after_compilation_2627221906.svg)
Multiple functions are fused into a single function, and constants are inlined.


Additionally, JIT helps us with the following:


- Improved L1, L2 cache usages.
- Less code to execute. It is placed on 1 page. Better usage of CPU branch predictor.
- Eliminate indirections.
- Multiple operations are fused in one function. The compiler can perform more optimizations.
- Using target CPU instructions (AVX256, AVX512\) if necessary. LLVM compiler can use the latest available instruction set for your CPU (AVX2, AVX512\) during compilation.


Improved usage of L1, L2 caches is important. If we check well\-known [table of numbers](http://norvig.com/21-days.html#answers), main memory reference is 20x times slower than L2 cache access, and 200x times slower that L1 cache access.


Consider such example `SELECT a + b * c + 5 FROM test_table`. This expression DAG `plus(plus(a, multiply(b, c)), 5)` is compiled into such LLVM IR:



```
define void @"plus(plus(UInt64, multiply(UInt64, UInt64)), 5 : UInt8)"(i64 %0, ptr %1) {
entry:
  %2 = getelementptr inbounds { ptr, ptr }, ptr %1, i64 0
  %3 = load { ptr, ptr }, ptr %2, align 8
  %4 = extractvalue { ptr, ptr } %3, 0
  %5 = getelementptr inbounds { ptr, ptr }, ptr %1, i64 1
  %6 = load { ptr, ptr }, ptr %5, align 8
  %7 = extractvalue { ptr, ptr } %6, 0
  %8 = getelementptr inbounds { ptr, ptr }, ptr %1, i64 2
  %9 = load { ptr, ptr }, ptr %8, align 8
  %10 = extractvalue { ptr, ptr } %9, 0
  %11 = getelementptr inbounds { ptr, ptr }, ptr %1, i64 3
  %12 = load { ptr, ptr }, ptr %11, align 8
  %13 = extractvalue { ptr, ptr } %12, 0
  %14 = icmp eq i64 %0, 0
  br i1 %14, label %end, label %loop

end:                                              ; preds = %loop, %entry
  ret void

loop:                                             ; preds = %loop, %entry
  %15 = phi i64 [ 0, %entry ], [ %26, %loop ]     /// PHI loop counter
  %16 = getelementptr i64, ptr %4, i64 %15        /// Adjust first argument ptr using loop counter
  %17 = load i64, ptr %16, align 8                /// Load first argument data from adjusted ptr
  %18 = getelementptr i64, ptr %7, i64 %15        /// Adjust second argument ptr using loop counter
  %19 = load i64, ptr %18, align 8                /// Load second argument data from adjusted ptr
  %20 = getelementptr i64, ptr %10, i64 %15       /// Adjust third argument ptr using loop counter
  %21 = load i64, ptr %20, align 8                /// Load third argument data from adjusted ptr
  %22 = mul i64 %19, %21                          /// Multiply second and third argument
  %23 = add i64 %17, %22                          /// Add first argument
  %24 = add i64 %23, 5                            /// Add constant 5
  %25 = getelementptr i64, ptr %13, i64 %15       /// Adjust result ptr using loop counter
  store i64 %24, ptr %25, align 8                 /// Write result value thought adjusted result ptr
  %26 = add i64 %15, 1                            /// Increment loop counter
  %27 = icmp eq i64 %26, %0                       /// Check if loop need to be terminated
  br i1 %27, label %end, label %loop              /// Terminate loop or jump to the next iteration
}

```

This LLVM IR can be represented as such code:



```
void aPlusBMulitplyCPlusConstant5(
    int64_t * a,
    int64_t * b,
    int64_t * c,
    int64_t * result,
    size_t size)
{
    for (size_t i = 0; i < size; ++i)
    {
        result[i] = a[i] + b[i] * c[i] + 5;
    }
}

```

And in result assembly, generated loop will look like this:



```

.LBB0_8:                                # %vector.body
    vmovdqu	(%r11,%rax,8), %ymm1
    vmovdqu	(%r9,%rax,8), %ymm3
    vmovdqu	32(%r11,%rax,8), %ymm2
    vmovdqu	32(%r9,%rax,8), %ymm4
    vpsrlq	$32, %ymm3, %ymm5
    vpsrlq	$32, %ymm1, %ymm6
    vpmuludq	%ymm1, %ymm5, %ymm5
    vpmuludq	%ymm6, %ymm3, %ymm6
    vpmuludq	%ymm1, %ymm3, %ymm1
    vpsrlq	$32, %ymm4, %ymm3
    vpmuludq	%ymm2, %ymm3, %ymm3
    vpaddq	%ymm5, %ymm6, %ymm5
    vpsllq	$32, %ymm5, %ymm5
    vpaddq	%ymm5, %ymm1, %ymm1
    vpsrlq	$32, %ymm2, %ymm5
    vpmuludq	%ymm2, %ymm4, %ymm2
    vpaddq	(%r14,%rax,8), %ymm1, %ymm1
    vpmuludq	%ymm5, %ymm4, %ymm5
    vpaddq	%ymm3, %ymm5, %ymm3
    vpsllq	$32, %ymm3, %ymm3
    vpaddq	%ymm3, %ymm2, %ymm2
    vpaddq	32(%r14,%rax,8), %ymm2, %ymm2
    vpaddq	%ymm0, %ymm1, %ymm1 /// in ymm0 there is constant 5
    vmovdqu	%ymm1, (%r10,%rax,8)
    vpaddq	%ymm0, %ymm2, %ymm2
    vmovdqu	%ymm2, 32(%r10,%rax,8)
    addq	$8, %rax
    cmpq	%rax, %r8


```


## ClickHouse compilation of aggregation [\#](/blog/clickhouse-just-in-time-compiler-jit#clickhouse-compilation-of-aggregation)


First, let’s see how aggregation looks like in the physical query plan:



```
EXPLAIN PIPELINE SELECT sum(UserID)
FROM default.hits_100m_single GROUP BY WatchID;

┌─explain────────────────────────────────┐
│ (Expression)                           │
│ ExpressionTransform                    │
│   (Aggregating)                        │
│   Resize 16 → 1                        │
│     AggregatingTransform × 15          │
│       StrictResize 16 → 16             │
│         (Expression)                   │
│         ExpressionTransform × 16       │
│           (SettingQuotaAndLimits)      │
│             (ReadFromMergeTree)        │
│             MergeTreeThread × 16 0 → 1 │
└────────────────────────────────────────┘

```

High level architecture looks like this:


![clickhouse_aggregation.svg](/uploads/clickhouse_aggregation_7ad2c6b91a.svg)
The Aggregate function interface looks like this:



```
class IAggregateFunction
{
    ...

    virtual ~IAggregateFunction() = default;

    /// AggregateDataPtr pointer to aggregate data for unique key during GROUP BY

    /// Create empty data for aggregation with `placement new` at the specified location.
    virtual void create(AggregateDataPtr place) const = 0;

    /** Adds a value into aggregation data on which place points to.
      * columns points to columns containing arguments of aggregation function.
      * row_num is number of row which should be added.
      */
    virtual void add(
        AggregateDataPtr place,
        const IColumn ** columns,
        size_t row_num,
        Arena * arena) const = 0;

    /// Merges state (on which place points to) with other state of current aggregation function.
    virtual void merge(AggregateDataPtr place, ConstAggregateDataPtr rhs, Arena * arena) const = 0;

    /// Inserts results into a column. This method might modify the state (e.g.
    /// sort an array), so must be called once, from a single thread.
    virtual void insertResultInto(AggregateDataPtr place, IColumn & to, Arena * arena) const = 0;

    ...
}

```

In general, the aggregate function is defined by its state and operations on this state:


- Creation of state.
- Add value to the state.
- Merge states. This operation is necessary if aggregation is performed using multiple threads.
- Materialize state as column value, and insert this materialized value into the result column. This operation is performed once at the end of aggregation.


For each aggregate function, state can be different. For example, for the `sum` function it can be just UInt64\. For `avg` function it can be UInt64 for sum and UInt64 for count, and during state materialization, the final value is computed as sum divided by count.


During the aggregation process for each unique aggregation key state is created and stored in hash table. We have a highly optimized hash table framework (which deserves a separate post) in which we store states of aggregate functions.


Now let’s take an example query:



```
SELECT sum(UserID)
FROM default.hits_100m_obfuscated
GROUP BY WatchID

```

In this example aggregation key is `WatchID`, and we have single `sum` aggregate function, and `UserID` is `sum` aggregate function argument.


During aggregation execution:


1. For each row, lookup aggregate state for aggregation key (in our case WatchID) in hash table. If aggregation state exists add the aggregate function argument value (in our case UserID) to the aggregation state. Otherwise, create the aggregate function state for this aggregation key, and add aggregate function argument value to aggregation state.
2. For each unique aggregation key merge the aggregate function states in case multiple threads are used for aggregation (most of the time in ClickHouse parallel GROUP BY operator processing is taking place).
3. For each unique aggregation key materialize the aggregate function state and insert the result into final column.


During these steps, we call:


- `create` aggregate function method for each unique key.
- `add` aggregate function method for each row.
- `merge` aggregate function method for each unique key.
- `insertResultInto` aggregate function method for each unique key.


The main problem is that we perform a lot of virtual function calls. The situation is even worse in the case of multiple aggregate functions because we have to perform the same number of virtual function calls as in the single function example, additionally multiplied by the number of aggregate functions.


Additional problems with this approach:


- For Nullable columns, we have a Nullable wrapper that wraps any aggregate function to work with nullable columns. This introduces an additional indirection layer.
- We also have aggregation combinators, like `-If`, `-Array`. They wrap any aggregate function and add specific logic. This introduces an additional indirection layer. Example: `SELECT sumIf(column, metric > value)`.


The solution is obvious, we need to fuse multiple aggregate functions into one. Basically, aggregate functions during aggregation use 4 actions: `create`, `add`, `merge`, `insertResultInto`. We can fuse these actions for multiple functions, to avoid indirections and decrease the number of virtual function calls.


The compilation is supported for the following aggregate functions:


- Most common aggregate functions `sum`, `count`, `min`, `max`, `avg`, `avgWeighted`.
- Nullable aggregate function adaptor.
- Aggregate function combinator `-If`.


For example if we take query:



```
SELECT
    sum(UserID),
    avg(ClientIP),
    sum(CounterClass),
    min(CounterID),
    max(WatchID)
FROM default.hits_100m_obfuscated
GROUP BY WatchID

```

Multiple aggregate functions will be fused into one:



```
SELECT
    sum_avg_sum_min_max(
        UserID,
        ClientIP,
        CounterClass,
        CounterID,
        WatchID)
FROM default.hits_100m_obfuscated
GROUP BY WatchID

```

## ClickHouse compilation of sorting [\#](/blog/clickhouse-just-in-time-compiler-jit#clickhouse-compilation-of-sorting)


First, let’s take a look how `ORDER BY` looks like in the physical query plan:



```
EXPLAIN PIPELINE SELECT WatchID FROM hits_100m_single
ORDER BY WatchID, CounterID;

┌─explain──────────────────────────────────┐
│ (Expression)                             │
│ ExpressionTransform                      │
│   (Sorting)                              │
│   MergingSortedTransform 16 → 1          │
│     MergeSortingTransform × 16           │
│       LimitsCheckingTransform × 16       │
│         PartialSortingTransform × 16     │
│           (Expression)                   │
│           ExpressionTransform × 16       │
│             (SettingQuotaAndLimits)      │
│               (ReadFromMergeTree)        │
│               MergeTreeThread × 16 0 → 1 │
└──────────────────────────────────────────┘

```

In physical query plan we have multiple transform that work together to perform sorting:


- PartialSortingTransform — sort single block, apply special optimization if LIMIT is specified.
- MergeSortingTransform — sort multiple blocks using k\-way\-merge algorithm, output of this transform is a stream of sorted blocks.
- MergingSortedTransform — sort multiple streams of sorted blocks using [k\-way\-merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm) algorithm.


Sort of single block in PartialSortingTransform, can be performed in batch, without indirections. There is `getPermutation`, `updatePemuration` methods in IColumn that returns or update permutation. This permutation can later be applied efficiently to any column using `permute` method.


The problem is with MergeSortingTransform and MergingSortedTransform. They must perform k\-way\-merge algorithm, and this algorithm operates on single rows instead of columns. In the worst case, we will apply `ORDER BY WatchID, CounterID` comparator to each row `N * log(N) * 2` times during our MergeSortingTransform, MergingSortedTransform.


Code example of IColumn `compareAt` and `sort` cursor `greaterAt` methods:



```
class IColumn
{
    ...
    virtual int compareAt(size_t n, size_t m, const IColumn & rhs, int nan_direction_hint) const = 0;
    ...
}

```


```
struct SortCursor : SortCursorHelper<SortCursor>
{
   using SortCursorHelper<SortCursor>::SortCursorHelper;

   /// The specified row of this cursor is greater than the specified row of another cursor.
   bool greaterAt(const SortCursor & rhs, size_t lhs_pos, size_t rhs_pos) const
   {
       for (size_t i = 0; i < impl->sort_columns_size; ++i)
       {
           const auto & sort_description = impl->desc[i];
           int direction = sort_description.direction;
           int nulls_direction = sort_description.nulls_direction;
           int res = direction * impl->sort_columns[i]->compareAt(lhs_pos, rhs_pos,
               *(rhs.impl->sort_columns[i]), nulls_direction);

           if (res > 0)
               return true;
           if (res < 0)
               return false;
       }

       return impl->order > rhs.impl->order;
   }
};

```

The worst thing for column DBMS is to process elements in rows. And the biggest problem here is that for each column specified in the `ORDER BY` comparator, we call `compareAt` method. We can fuse multiple `compareAt` methods in a single function to avoid unnecessary indirections and decrease the number of virtual function calls if multiple columns are specified in the comparator.


For Nullable columns, performance could be even better because in implementation of its `compareAt` method, it first checks nulls, and if both values are not null, uses inner column `compareAt` method.


## JIT complication costs [\#](/blog/clickhouse-just-in-time-compiler-jit#jit-complication-costs)


Now, what about compilation costs? JIT compilation time of expressions, aggregate functions, or ORDER BY comparator is around 5\-15 ms and grows linearly with code size. On average compiled function uses 1 page for the code section and 1 page for the data section. 4096 \* 2 \= 8192 bytes on most configurations.


Introspection works inside ClickHouse using `CompileExpressionsMicroseconds`, `CompileExpressionsBytes` metrics that are available for each query.



```
SELECT
    ProfileEvents['CompileExpressionsMicroseconds'] AS compiled_time,
    ProfileEvents['CompileExpressionsBytes'] AS compiled_bytes
FROM system.query_log
WHERE compiled_time > 0;

┌─compiled_time─┬─compiled_bytes─┐
│         16258 │           8192 │
│         26792 │           8192 │
│         15280 │           8192 │
│         11594 │           8192 │
│         14989 │           8192 │
└───────────────┴────────────────┘

```

In ClickHouse we perform a compilation of expressions only when we see some number of the same repeated expressions. The same applies to aggregate functions and ORDER BY comparators. This number can be controlled using `min_count_to_compile_expression`, `min_count_to_compile_aggregate_expression`, `min_count_to_compile_sort_description settings`, by default their values equals 3\. To avoid unnecessary recompilation, we use the LRU cache for the JIT\-compiled code.


## Summary [\#](/blog/clickhouse-just-in-time-compiler-jit#summary)


JIT compilation can transform dynamic configuration into static configuration:


- Compile evaluation of multiple expressions. Example: `SELECT a + b * c + 5 FROM test_table;`.
- Compile aggregate functions in GROUP BY operator. Example: `SELECT sum(a), avg(b), count(c) FROM test_table;`.
- Compile comparator in ORDER BY. Example: `SELECT * FROM test_table ORDER BY a, b, c;`.


In all cases, we transform dynamic configuration into static.


Not all functions and algorithms can be easily compiled. JIT compilation has its own costs: compilation time, memory, and maintenance. But nevertheless, it can greatly improve performance in a lot of special cases where it can be applied.


In ClickHouse, JIT compilation for expression evaluation improves performance in 1\.5\-3 times (for some cases, more than 20 times). JIT compilation for aggregation improves performance in 1\.15\-2 times. JIT compilation for ORDER BY comparator improves performance in 1\.15\-1\.5 times.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
