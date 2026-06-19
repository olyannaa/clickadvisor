CREATE TABLE lineitem (
    l_orderkey      UInt32,
    l_partkey       UInt32,
    l_suppkey       UInt32,
    l_linenumber    UInt8,
    l_quantity      Decimal(15,2),
    l_extendedprice Decimal(15,2),
    l_discount      Decimal(15,2),
    l_tax           Decimal(15,2),
    l_returnflag    FixedString(1),
    l_linestatus    FixedString(1),
    l_shipdate      Date,
    l_commitdate    Date,
    l_receiptdate   Date,
    l_shipinstruct  String,
    l_shipmode      String,
    l_comment       String
) ENGINE = MergeTree()
ORDER BY (l_shipdate, l_orderkey, l_linenumber)
PARTITION BY toYYYYMM(l_shipdate);

CREATE TABLE orders (
    o_orderkey      UInt32,
    o_custkey       UInt32,
    o_orderstatus   FixedString(1),
    o_totalprice    Decimal(15,2),
    o_orderdate     Date,
    o_orderpriority String,
    o_clerk         String,
    o_shippriority  UInt8,
    o_comment       String
) ENGINE = MergeTree()
ORDER BY (o_orderdate, o_orderkey)
PARTITION BY toYYYYMM(o_orderdate);

CREATE TABLE customer (
    c_custkey    UInt32,
    c_name       String,
    c_address    String,
    c_nationkey  UInt32,
    c_phone      String,
    c_acctbal    Decimal(15,2),
    c_mktsegment String,
    c_comment    String
) ENGINE = MergeTree()
ORDER BY c_custkey;

CREATE TABLE part (
    p_partkey     UInt32,
    p_name        String,
    p_mfgr        String,
    p_brand       String,
    p_type        String,
    p_size        UInt8,
    p_container   String,
    p_retailprice Decimal(15,2),
    p_comment     String
) ENGINE = MergeTree()
ORDER BY p_partkey;

CREATE TABLE supplier (
    s_suppkey   UInt32,
    s_name      String,
    s_address   String,
    s_nationkey UInt32,
    s_phone     String,
    s_acctbal   Decimal(15,2),
    s_comment   String
) ENGINE = MergeTree()
ORDER BY s_suppkey;

CREATE TABLE partsupp (
    ps_partkey    UInt32,
    ps_suppkey    UInt32,
    ps_availqty   UInt32,
    ps_supplycost Decimal(15,2),
    ps_comment    String
) ENGINE = MergeTree()
ORDER BY (ps_partkey, ps_suppkey);

CREATE TABLE nation (
    n_nationkey UInt32,
    n_name      String,
    n_regionkey UInt32,
    n_comment   String
) ENGINE = MergeTree()
ORDER BY n_nationkey;

CREATE TABLE region (
    r_regionkey UInt32,
    r_name      String,
    r_comment   String
) ENGINE = MergeTree()
ORDER BY r_regionkey;
