## Databricks Certified Associate Developer for Apache Spark - Free Prep Materials

- [X] **Check Databricks Certification Exam Guide (official PDF)** - lists exact topics, weightings, and the Spark version: https://www.databricks.com/learn/certification/apache-spark-developer-associate
- [X] Databricks Academy - Self-paced Module: Introduction to Python for Data Science and Data Engineering 
- [X] Databricks Academy - Self-paced Module: Introduction to Apache Spark™
- [X] Databricks Academy - Self-paced Module: Developing Applications with Apache Spark™
- [ ] Databricks Academy - Self-paced Module: Stream Processing and Analysis with Apache Spark™
- [ ] Check This PDF: https://www.databricks.com/sites/default/files/2025-10/databricks-certified-associate-developer-apache-spark-exam-guide-oct-2025.pdf
- [ ] **Apache Spark official documentation - Structured API / SQL guide** - primary reference for DataFrame transformations, which make up most of the exam. https://spark.apache.org/docs/latest/sql-programming-guide.html
- [ ] **PySpark API reference** - know `pyspark.sql.functions`, `DataFrame`, and `Column` methods well: https://spark.apache.org/docs/latest/api/python/reference/index.html
- [ ] **Databricks Free Edition** - free workspace to practice hands-on instead of just reading (replaces Community Edition). https://www.databricks.com/learn/free-edition
- [ ] **CertifHub - Databricks Associate Developer for Apache Spark Study Guide 2026** - free community-written study
  guide summarizing topics. https://blog.certifhub.com/databricks-certified-associate-developer-for-apache-spark-3-0-study-guide-2026/
- [ ] **FlashGenius - Ultimate Guide to the certification** - free blog with exam tips and a study plan.
  https://flashgenius.net/blog-article/ultimate-guide-to-databricks-certified-associate-developer-for-apache-spark-certification

## Sample Exam Questions

- Databricks Certified Associate Developer for Apache Spark
    - certshero: https://certshero.com/databricks/databricks-certified-associate-developer-for-apache-spark-3.5/practice-test
    - ExamTopics: https://www.examtopics.com/exams/databricks/certified-associate-developer-for-apache-spark/view/
    - ITExams: https://www.itexams.com/exam/Certified-Associate-Developer-for-Apache-Spark
    - p2pexams: https://www.p2pexams.com/databricks/pdf/databricks-certified-associate-developer-for-apache-spark-3.5
    - CertSafari: https://www.certsafari.com/databricks/developer-for-apache-spark-associate

## Databricks Platform Notes

- Databricks Catalog 3-Folded Structure `catalog.schema.data-object`

## Spark Intro

- Main Features:
    - Distrubuted and open-source
    - Supports SQL/streaming/ML/graph processing
    - Connects to Data Sources: Cloud (AWS S3, Azure, Google), file systems, databases

- You can use `pyspark.pandas` api for pandas-like syntax in Spark for Spark DF
- Both Side Possible: `PySpark DF` <> `Pandas DF`
- Spark Index Types:
    1. `sequence` (Default): `0-1-2-...`, bad for large data, risk of whole partition on 1 node.
    2. `distributed-sequence`: Sequence mode with group-by + and group-map in a _distributed_ manner
    3. `distributed`: `monotonically_increasing_id` in _distributed_ manner, non-deterministic, no sequence

## Spark Engine and API Levels

0. Spark Core Engine (RDD API): Mem Manage, Scheduling, Task Distribution, Fault Recovery.
1. Dataframe API: High-level API for structured data ops.
2. Libraries: Structured Streaming API, MLLib, Spark SQL, SparkR API, Graphx (this goes to Spark Core)

## Spark Runtime Components

- **Client (or Job)**
- **Driver**: Brain of Spark Apps
    - Interacts with Client/job
    - `SparkSession`: Entry point for all Spark apps, unifies `(Spark|SQL|Hive|Streaming)Context`
    - DAG and Planning: Analyzes Spark app and creates a DAG
    - DAG Stages: Task groups that can be executed in parallel
    - Coordination Execution: Schedule and distribute jobs to _Executors_
    - Monitoring: task progresses
    - Failure Handling
- **Cluster Manager (Master Node)**:
    - manages cluster resources
    - allocates cluster resources to Driver
- **Executors in Worker Node**:
    - Hierarch: 1 Worker <> N Executors <> NxM Tasks
    - Limited by `spark.executor.cores` (cpu), `spark.executor.memory`, config settings
    - Execute Tasks given by Driver: I/O & Data Processing
    - Caching: Store intermediate/final results in Mem or on Disk
    - Report to Driver: for results
- **Spark UI**: Web UI for management & monitoring
    - App UI per App (`SparkSession`): DAG viz, stage details, resource usage, performance metrics
    - Master UI per Cluster: Worker node status, node health, cluster resource alloc, running apps

## Spark App Execution

- Spark App -> N Jobs
- Job -> M Stages (Sequential Execution)
- Stage -> Z Tasks & Z Partitions (Parallel/independent Execution)

## Spark Clusters in Databricks

1. All Purpose Clusters: interactive, notebooks, jobs, dashboard, configurable auto-termination
2. Job Clusters: non-interactive, ephemeral, start-run-terminate
3. SQL Warehouses (serverless): optimized for SQL query performance, instant start-up, auto-scale for cost/performance,
   no cluster management

## Spark DF (DataFrame) Intro

- Distributed collections of records with the same schema
- Schema: pre-defined structure, every DF has it, can be specified (more efficient, e.g. Parquet) or inferred
- Supports SQL funcs, relational operators
- Lazy Evaluation & DAG: only if necessary, fault tolerance, lineage
- Creation Source: Delta Lake, txt, RDD, csv, json, parquet, orc, a catalog table/view, DB

## Spark DF API Optimizations

- Adaptive Query Optimization: dynamic/cost-effective runtime plan, based on data characteristics & execution patterns
- Tungsten (In-Mem Columnar Storage Engine): better query performance, less memory footprint
    - Off-Heap Mem Management
    - Cache-Aware Computation
    - Code-generation for faster execution
    - Whole-Stage Code Generation
- Built-in Stats: collects auto-stats when saving to optimized formats (Parquet, Delta) for smarter planning & execution
- Catalyst Query Optimization Engine:
    - Converts DF -> Optimized Execution Plan
    - Uses rule/cost-based optimizations
- Photon Vectorized Query Engine:
    - Better query execution
    - Batches: Data processing in batches (not row-by-row)
    - In Dbricks Clusters: SQL WH (default), All-Purpose Clusters (opt-in), Job Clusters (opt-in)

## Spark DF/Query Planning

- Used by Driver for _efficient physical execution plan_
- Transformation Steps:
    1. Unresolved Logical Plan (Analysis)
    2. Analyzed Logical Plan (Logical Optimizations)
    3. Optimized Logical Plan (Physical Optimizations)
    4. Physical Plan (Code Gen)

## Spark DF Data I/O, Schema, Data Types

- DataFrameReader: multiple input formats
- DataFrameWriter: allows partitioning, save modes (overwrite, append), flexible output formats
- DDL (Data Definition Language) Schema: alternative to `StructType`, example:
  `name STRING NOT NULL, height INT, eye_color STRING`
- Data Types: `pyspark.sql.types.DataType`  vs Spark SQL
    - (omitted `Type` suffix): Byte, Short, Integer, Long, Float, Double, Boolean, String, Binary, Timestamp, Date,
      Array, Map, Struct
    - Spark SQL              : `tinyint`, `smallint`, `int`, `bigint`, float, double, `bool`, string, binary, timestamp,
      date, array, map, struct

## Spark DF Transactions and Actions

- DFs are Immutable: modification creates new DFs
- `Transformations`: Creates DF' from DF, evaluated lazily until action
    - Examples: `select()`, `filter()`, `withColumn()`, `groupBy()`, `agg()`
- `Actions`: Trigger actual computation & produce results
    - Examples: `count()`, `show()`, `take(n)`, `first()`, `write()`

## Spark SQL Metastore and DF Integrations

- Speed Comparison of Spark SQL vs DF: They are the same!
- Metastore:
    - Holds: properties/information for tables/views/funcs
    - Defines: schema, locations, partitions
    - Unity Catalog in Dbricks: Centralized, fine-grained security/governance across all data
- Register a DF to SQL: Temp Views (`createOrReplaceTempView("name")`), Global Temp Views (
  `createGlobalTempView("name")`)
- SQL Query Execution: `spark.sql()`, seamless DF/metastore integration, built-in functions 

## Spark UDFs (User Defined Functions)
- Reusable Custom Python functions
- Cannot be optimized by Catalyst Optimizer
- Have serialization overhead (Python <> JVM)
- Best to Worst: Built-ins > Pandas UDF (with Arrow, Serialization) > Custom UDF

## Distributed Systems Programming Fundamentals

+ Shared Noting Architecture
  - Benefits: lower retention, parallel processing, high throughput, low latency
  - Independence: each node runs independently with CPU, memory, disk  
  - Scalability: each new node helps performance without resource contention
  - Fault Tolerance: Each fault in each node is confined (no system-wide effect)
  - Resource Partitioning: data/workload are partitioned across nodes

+ Data Partitioning: Data Distribution
  - Mutually exclusive in-memory partitions
  - Default Value: based on input, configurable
  - Parallelism: affected by `size(partitions)` and `num(partitions)`

+ Data Partitioning: Processing Model
  - Parallel and Independent: Each partition can run in parallel
  - Spark: 1 Task = 1 Partition
  - Performance Tuning: reduce shuffle, tune partitions

+ Shuffle Operation
  - Definition: data redistribution across partitions, most expensive op in Spark, e.g. `groupBy`, `join`
  - Occurs when: wide transformations, key-based ops, data repartitioning

+ Map-Reduce
  - Map Stage: `select()`, `filter()`, projection
  - Shuffle Stage: most expensive!
  - Reduce Stage: aggregation/final transformation on shuffled data 

+ Spark's Implementation
  - Map/Shuffle/Reduce: core building block for every Spark op, even simple transformations
  - Examples:
    - `groupBy`: Map (extract keys) -> Shuffle (by key) -> Reduce (aggregate)
    - `join`: Map (prepare keys) -> Shuffle (co-locate) -> Reduce (Combine)
    - `filter`: Map (evaluate condition)


## Spark Coding Details

+ `groupBy`: Supports 1+ cols/patterns, parallel across partitions, lazily evaluated
+ `agg`: Supports Pandas UDFs, bulk aggregate with dict `df.groupBy("x").agg({"col1":"sum","col2":"avg"})`
+ Windows Funcs:
```python
windowSpec = pyspark.sql.window.Window.partitionBy("col1").orderBy("col2")
df.withColumn("new_col_1", rank().over(windowSpec)) \
  .withColumn("new_col_2", sum("salary").over(windowSpec)) \
  .withColumn("new_col_3", lag("salary").over(windowSpec)) \
  .withColumn("new_col_4", ntile(6).over(windowSpec)) # Divide into 6 tiles
```

+ Joins:
```python
df1.alias("my_df1").join(
  df2.alias("my_df2"),
  on=[df1.x == df2.y, ...], # list[Condition] | Condition
  how="left" # Literal["left","right","inner","outer"]
)
```

+ Join Performance
  + Spark choses the join strategy, better to use small DFs first
  + Broadcast Join: Spark can broadcast the small DF to all worker nodes 

+ Data Skew Handling: uneven join keys is bad performance, consider repartitioning some time

+ Memory Management:
  + Monitor shuffle spills for joins
  + Cache frequently joined DFs
  + Projection: use only necessary columns


## Spark Complex Types and Functions

+ Structs:

```python

df.select(col("User").getField("name")) # .getField()
df.select(col("User.name")) # Direct dot
df.select(col("User.scores")[0].alias("first_score")) # Nested access

```

+ Unnesting array with `explode()`: expensive, creates 1 row per array element

+ Common Array Column Ops: `array_contains(col,val)`, `size(col)`, `element_at(col,n)` (1-indexed), `array_distinct(col)`
+ Aggregate to Arrays: `collect_list()` (often used with `groupBy`), `collect_set()` (no duplicates, memory efficient), both expensive
+ `pivot()`: Creates N-Hot Encoding (columnar) out of arrays  


## Spark Structured Streaming (2018->) Basics

+ Microbatching: ~100ms-3s chunks, core of distributed stream processing
+ Streaming Use Cases: Fraud Detection, Anomaly Detection, Live Dashboards, Clickstream Analysis, Sensor&IoT Monitoring
+ Not All Stream Processing cases are real-time 
+ Spark Streaming (2013): Uses RDD API, `DStream` (Discretized Streams) model, processing in small time-based batches

+ Streaming Data = Each row appended to Infinite Table
+ Continuously Updated Queries
+ Supports DF/DS APIs (same as batch processing)
+ Event-time processing
+ Watermark support for late data
+ End-to-end exactly-once guarantees (no data loss, no duplication)
+ Simplified, supports SQL ops, handles out-of-order data better

+ Databricks Autoloader(cloud_files): auto-schema handling and high performance 
+ Transformation Logic: same as batch
+ Implementation: 
  - `DataStreamReader`, `DataStreamWriter`
  - `df.writeStream().start("outPath")`
  - `devices_query.stop()`, `devices_query.awaitTermination()`


+ Triggers: Latency-Throughput Tradeoff 
  - Default Triggers: Process microbatch as soon as the previous one completes, example: `df.writeStream.start()` 
  - Fixed Interval Triggers: At specified time intervals, useful for resource control, example: `df.writeStream.trigger(processingTime="2 minutes").start()`
  - Available Now Triggers: One time data processing no repeating, example: `df.writeStream.trigger(availableNow=True).start()`

+ Output Modes
  - `append` (default): stateless, add new records to sink, queries w/o agg
  - `update`: modifty existing records, only outputs changed records after last processing
  - `complete`: entire result table to sink each time, good for aggregations/running totals/leaderboards

+ Monitoring Streams
  + Spark UI: Stream tab for active queries, progress details per batch
  + External Monitoring Tools: processing rates/latency, memory usage, GC, examples: Datadog, Grafana, Prometheus
  + Useful Inspection Funcs: `df.isStreaming`, `query.id`, `query.status`, `query.lastProgress`


## Spark Structured Streaming Advanced

+ Stateful vs Stateless Ops
  - Stateless: process each record independently, no previous memory, examples: `select`, `filter`
  - Stateful: maintain info across batches, needs checkpoint locations, Window ops, examples: `join`, `dropDuplicates`, `groupBy`

+ Checkpoint Location is needed, because
  - Maintain state across batches
  - Fault Tolerance: recover state in case of failure
  - Handle replay of data without replicates

+ Challenges in Distributed State and Distributed Data
  - Needs Fault tolerance for state recovery
  - Memory limitations of large state
  - Consistency across node failures 

+ RocksDB Backend:
  - Persistence with ⬆️ Performance
  - Builtin state store for Spark Structured Streaming
  - Features: efficient storage/retrieval, auto compaction, supports large state sizes

+ Streaming Joins
  - Streams can join with: streamingDF, staticDF (normalDF, complete output of streamingDF)
  - Supported Join Types: all except `full`, `cross`
  - Memory usage high due to keeping states
  - Defined Intervals: Needed for both Streams

+ Streaming Aggregations:
  - Types: `count`, `min/max`, `sum/avg`
  - Approx Funcs performs better: `approx_count_distinct()`

+ Window Funcs:
  - Timestamp should be in the data (if not, create)
  - Time-based: Tumbling (non-overlapping, fixed)
  - Time-based: Sliding (can overlap)
  - Activity-based: Session (dynamically sized, with gaps/timeouts)

+ Window Func Implementation:
  - Sliding Windows:
  ```python
  sliding_windows = df.groupBy(
    window(col("time_col"), windowLength="2 minutes", slideInterval="1 minute"),
    col("order_status")
  ).count()
  ```
  - Auto Generated Output Columns: `window_start`, `window_end`
  - With Watermarks:
  ```python
  status_events.withWatermark(eventTime="event_timestamp", delayThreshold="10 minutes").groupBy("...")
  ```
  - Stop a streaming query and wait for the final batch to complete processing:
  ```python
  query.stop() and query.awaitTermination()
  ```
+ Handling Late Data
  - Watermark: Grace period to wait, drops anything after this
  - ⬆️ Watermark = ⬆️ Correction, Bad Memory, Bad Latency. 
  - ⬇️ Watermark = ⬇️ Correction (can drop late events), Good Memory, Good Latency. 
