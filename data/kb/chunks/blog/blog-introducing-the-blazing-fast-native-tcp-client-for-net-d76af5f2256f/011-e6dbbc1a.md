---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-the-blazing-fast-native-tcp-client-for-net-clickhouse
ch_version_introduced: '10.0'
last_updated: '2026-10-26'
chunk_index: 11
total_chunks_in_doc: 14
---

offset), control).StoreUnsafe(ref dst, offset); 7} ``` Copy command In our micro\-benchmark that’s about 9× faster than moving the bytes one at a time, and it allocates nothing. Machines without vector support fall back to a plain scalar loop.

One thing worth knowing if you try this yourself: on .NET 8 and 9, `Shuffle()` only becomes `vpshufb` when the JIT can see that the control vector is a constant. Our loop takes the control as a parameter, and it still gets `vpshufb` because the JIT inlines it into a caller where the `static readonly` field is visible. Pass a plain parameter into a method that isn’t inlined, and you get a call to a software fallback instead. .NET 10 accelerates both. You can check your own code with `DOTNET_JitDisasm`.

#### QBit: vectors stored sideways. \#

ClickHouse’s `QBit(T, N)` type exists to speed up approximate vector search. It takes N floating point values and stores them with one plane per bit (32 for float32\), most significant first, so a distance function like `L2DistanceTransposed(vec, ref, p)` can read only the first `p` bits of each element and trade precision for speed. On insert, the client has to do that transpose:

![](/_next/image?url=%2Fuploads%2Ffig_qbit_28d6ab5ed3.png&w=2048&q=75)

Done one bit at a time, that’s 32 ops per element. With `Vector256`, `ExtractMostSignificantBits` collects the top bit of 8 floats into one byte, which is exactly one plane byte, already in the wire’s bit order. Shift every lane left by one, and the next bit is on top:

```
1Vector256<uint> lanes = Vector256.LoadUnsafe(ref source, (nuint)(group << 3));
2int slot = rowBase + QBitLayout.ByteOfGroup(group, BytesPerRow);
3for (int wireIndex = 0; wireIndex < BitWidth; wireIndex++)
4{
5    scratch[(wireIndex * planeStride) + slot] = (byte)lanes.ExtractMostSignificantBits();
6    lanes <<= 1;
7}
```
Copy command
The JIT turns that loop body into one `vmovmskps` and one `vpslld`. It made the write path 11\.7× faster at 1,024 dimensions and 16\.5× faster at 768\.

### Where zero\-copy was not possible \#

Zero\-copy is the rule, but when the wire format and the .NET memory layout disagree (or when we have to instantiate an object), it is not possible.
