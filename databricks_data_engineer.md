# Databricks - Data Engineering Plan

## Intro to Data Engineering in Databricks (dbx)

+ 3 Components of Databricks Lakeflow:
	- Lakeflow Connect: Ingestion connectors for apps, DBs, cloud storage, message busses, local files
	- Spark Declarative Pipelines: Framework for batch/streaming data pipelines via SQL/Python
	- Lakeflow Jobs: Workflow automation to orchestrate data processing, coordination of 1+ tasks in complex workflows

## Lakeflow (LF) Connect

+ LF Connect - Benefits
	- Managed & Efficient Solution: Low cost, quick time-to-value
	- Self-Serve Interfaces: Easy, democratized, fast innovation
	- Unified Observability & Governance: Secured/healty pipelines & tables

+ LF Connect - Connectors
	- Upload Files: local file to dbx/volume, create table from local file
	- Standard Connectors: Sources (Cloud Object Storage, Kafka, etc.), Ingestion Methods (Batch, Incremental Batch, Streaming)
	- Managed Connectors: Sources (SaaS apps, DBs), incremental read/writes, faster/scalable/cost-efficient

+ LF Connect - Ingestion Methods
	- Batch Ingestion: load data as row batches into dbx, process all records in each run, simpler, better for large data, usuall scheduled, sql=`CREATE TABLE AS SELECT`, python= `spark.read.load()`
	- Incremental Batch Ingestion: ingest only new data automatically, skip loaded data, faster/resource-effective, sql=`COPY INTO`, python=`spark.readStream` (autoloader + timed-trigger), declarative-pipelines=`CREATE OR REFRESH STREAMING TABLE`
	- Streaming Ingestion: sources (Kafka, Kinesis, Google sub/pub, Pulsar), continuous load, ~real-time querying, micro-batch small short/frequent intervals, python=`spark.readStream` (autoloader + continuous-trigger), declarative-pipelines=`trigger-mode continuous`

## Delta Lake & Medallion Structure Review

+ Delta Lake Overview
	- An open-source protocol for reading and writing files to cloud storage
	- Supports Lakehouse architecture
	- Supports storage on AWS, Azure, GCP

+ Delta Table Components
	- Parquet Files: Store data within a folder directory
	- Delta Logs: in JSON, tracks transactions and table versions

+ Delta Table Key Features
	- ACID: allows read/wwrite concurrency among 1+ users w/o conflicts
	- DML (Data Manipulation Language): Supports flexible DML ops like INSERT, UPDATE, DELETE, MERGE
	- Time Travel: auditing, recovery, Query/revert to previous versions of data
	- Schema Evolution & Enforcement: enforces defined schema for data integrity, allows schema evolution
	- Unified batch/streaming processing, performance optimization, scalability
	- Transaction Log: records eacxh insert/update/delete, reliable data views

## Data Ingestion from Cloud Storage

+ Cloud Storage to Ingestion:
	- From Raw Files: CSV, JSON, Parquet, etc.
	- To Delta Tables
	- Performed by: LF Connect Standard Connectors

+ Ingestion Method - CTAS (CREATE TABLE AS) + `spark.read`
	- Ingestion Type: Batch
	- Best for: one-time, ad hoc ingestion. Can be scheduled to always read and process all data.
	- Schema Evolution: Manual or inferred during read
	- Scale: Small datasets
	- Idempotency: NO
	- Unified schema: Can be inferred
	- Can be used with streaming-tables via autoloaders
	- SQL: `<CTAS> SELECT * FROM read_files(path,format,**);`
	- PYTHON: `spark.read_files`

+ Ingestion Methods - COPY INTO
	- Ingestion Type: Incremental Batch
	- Best for: Simple and repeatable for incremental file ingestion. Great for scheduled jobs or pipelines.
	- Schema Evolution: Supported with options
	- Scale: Thousands of files
	- Latency: moderate (scheduled)
	- Idempotency: YES
	- FORMAT_OPTIONS()=source-parsing/interpretation
	- COPY_OPTIONS()=`mergeSchema`(schema evolution)
	- `force` (idempotency)
	- SQL: `COPY INTO tbl FROM 'cloud_dir_path' ...`
	- Python: -

+ Ingestion Method - AutoLoader
	- Ingestion Type: Incremental batch or streaming ingestion
	- Best for: near real-time streaming or incremental ingestion, with high automation and scalability.
	- Schema Evolution: Automatically detects and evolves schemas. Handles new columns as they appear.
	- Scale: Millions/billions files per hour
	- Idempotency: YES
	- Latency: low or high depending on config
	- Simple, scalable, relies on Spark Structured Streaming
	- Streaming Tables: recommended over `copy into`, registered in UC, comes with a pipeline, supports Kafka and Cloud Object Storage
	- SQL (Declarative Pipelines): Use `read_files` + `STREAM`, `CREATE OR REFRESH STREAMING TABLE tbl SCHEDULE EVERY 1 HOUR AS SELECT * FROM STREAM read_files()`
	- Python: `spark.readStream.format("cloudFiles").**.load("vlm").writeStream.trigger(processingTime="5 seconds").toTable("ctlg.db.tbl")`

## Working `_metadata` and `_rescued_data` Columns on Ingest

+ Benefits of adding Metadata Columns
	- Debugging
	- Lineage
	- Auditing

+ `_metadata` Column:
	- Hidden by default
	- Available for all input file
	- Its fields need to be selected in read query

+ Common `_metadata` Fields to Add
	- Source/Input File Name: `_metadata.file_name`
	- Last Modification Timestamp of Input File: `_metadata.file_modification_time`

+ `_rescued_data` Column Features
	- Created by: `SQL::read_files()`, `spark.read`, or AutoLoader
	- JSON Strings: Stored mismatched values
	- `null`: no mismatch
	- Prevents silent data loss
	- In `PYTHON::spark.read` add `.option("rescuedDataColumn","_rescued_data")`
	- In `SQL::read_files()` add `rescueddatacolumn => "_rescued_data"`

## Ingesting Semi-Structured Data: JSON

+ JSON Format:
	- Object: `{}`
	- Key: type=string, always contains value, `"key":"value"`
	- Value: str, num, bool, array, obj, null

+ JSON String Column Methods
	- String: raw text, no constraints, less performant `json_col:name`, `json_col:address:city`
	- Struct: defined schema, more query efficient, more consistent
	- Variant: can store any type of data, high flexibility, better performance

+ Implementation - Struct from JSON String
	- `STRUCT<>`
	- `ARRAY<>`
	- `json_key: {TYPE}`
	- `{TYPE}`: INT | STRING | STRUCT<> | ...
	- Array of Structs: `STRUCT< ARRAY< key_a:T1, key_b:T2 > >`
	- Function `schema_of_json()`: From a sample JSON str, `SELECT schema_of_json('a-json-str')`
	- Function `from_json()`: Converts struct-string to strusct_col, `SELECT from_json(json_col, 'json-struct-schema') AS struct_col FROM tbl`
	- Access: `struct_col.item`

+ Implementation - Variant from JSON String
	- Function `parse_json ( json_str )`
	- Access and Easy Cast: `variant_col:item :: STRING`

+ BASE64 Values: use `CAST( unbase64(base64_col) AS STRING )`

+ Struct Array Functions:
	- Explode: `explode( value.items ) AS item_in_array`
	- Array Length: `array_size( value.items ) AS num_elements`

## Ingesting Enterprise Data Overview

+ LakeFlow Connect Managed Connectors
	- Ingest data from DBs (SQLs, SQL Server), Apps (Workday, Salesforce)
	- Simple: UI, low-code, can via API
	- Reliable & Fast

+ SaaS Apps - Managed Ingestion Pipeline Steps
	1. Collect Credentials: LF Serverless Declarative Pipelines job collects credentials from UC.
	2. Reach Public Data Source: e.g. API, open OLAP port
	3. Streaming Data Table: final storage

+ DB Ingestion - Architecture Steps
	1. Classic Compute DP: Collects creds from UC
	2. Ingestion Gateway: Connect/Collect Data ( metadata, snapshots, change logs) from DB sources
	3. UC Volume as Staging Layer: Stores staging data and states, secure
	4. Serverless DP: Processes collected data to Streaming Delta Tables

+ DB Ingestion - Gateway
	- Decreased Network Load on DB
	- Network Isolation
	- Reliable Recovery Matter
	- Prevents continuous DB connectivity

+ Data Ingestion with Partner Connect
	- For other data sources
	- Create trial accounts via dbx
	- Test and Evaluate
	- Example Partners: informatica, prophecy, fivetran, Qlik, rivery, alteryx

## Additional Features and Ingesting into Existing Delta Tables

+ Lakehouse Federation
	- Query external data sources
	- No data moving
	- Good for: Ad-hoc reporting, exploratory phase
	- Support workloads during incremental migration

+ Zerobus
	- LF Connect API
	- Write event data to LH directly
	- High throughput, low latency
	- Simple Ingestion for: IOT, Clickstreams, Telemetry

+ Delta Sharing
	- Share data across platforms, clouds, regions
	- Secure

+ Dbx Marketplace
	- Open exchange for all data products (datasets, notebooks, ml models, etc.)
	- Get Instant Access

+ MERGE INTO Features
	- Automatic update, insert, delete in an existing Delta table
	- Schema Enforcements: Supported
	- Schema Mismatch: Fails by default
	- Schema Evolution: Supported with `MERGE WITH SCHEMA EVOLUTION INTO`
	- Matched Rows: UPDATE or DELETE
	- Unmatched rows by target: INSERT
	- Unmatched rows by source: UPDATE or DELETE
	- Good For: SCD (Slowly Changing Dimension), incremental loads, complex CDC (Change Data Capture)

+ MERGE INTO SQL Example:

```sql
MERGE INTO target_table target
USING source_table source
ON target.id = source.id
WHEN MATCHED AND source.status = 'update' THEN
  UPDATE SET
    target.email = source.email,
    target.status = source.status
WHEN MATCHED AND source.status = 'delete' THEN
  DELETE
WHEN NOT MATCHED THEN
  INSERT (id, first_name, email, sign_up_date
  status)
```

## LF Jobs Core Components

+ LF Job:
	- Scheduling
	- Coordinating
	- Run operations: Data processing, ETL, analytics, ML
	- Contains: 1+ tasks
	- Supported Langs: SQL, Python, Scala, Java (via JAR), R

+ LF Task:
	- Single unit of work in a Job
	- Examples: Notebook, script, query, dbt, spark, py-wheels etc.
	- Each task's compute source can differ

+ LF Task Common Options:
	- Path
	- Libs
	- Params
	- Notification
	- Retry Policies

+ LF Task Type Options:
	- Notebook: Source Path, Compute Options (cluster config), etc.
	- SQL: Task Name, SQL query, SQL warehouse

+ LF Task Control Flow Executions
	- Sequential
	- Parallel
	- Conditional (if/else)
	- Modular
	- Iterative (for each)

+ LF Task Trigger Types	
	- Manual: On-demand
	- Scheduled: Cron
	- API: Programmatic exec
	- Event-driven: On file-arrival
	- Table: Fata change events
	- Continuous: Streaming workload

+ LF Job Compute Options
	- Interactive / All-Purpose Clusters: shared, multi-user, expensive, no-prod, best for ad-hoc analysis / data-exploration / development
	- Job Clusters: 50% cheaper, lifetime bound to job, prod-grade, subject to cloud provider start-up times, can be reused across tasks
	- Serverless: fully managed, auto-scaling, optimized performance, simple, fast, reliable, cheap, better UX, performance-mode for faster job start-up/exec
	- SQL WH: for sql queries, for dashboards, for BI, can use notebooks, low latency, high concurrency, autoscaling, auto-start/stop, adjustable cluster size, cost-control

+ LF Task Orchestration and DAG
	- DAG (Direct Acyclic Graph): no cycles, task dependencies
	- Run Multiple Tasks as a DAG
	- Orchestrate tasks: via Dbx-UI, API, SDK, or Dbx Asset Bundles

+ LF Tasks - Common Workloads Patterns
	- Sequence: data transformation, processing, cleaning. Example: bronze -> silver -> gold
	- Funnel: `{A,B,C}` -> `{D}`, data collection/consolidation from 1+ sources
	- Fan-out / Star: `{A}` -> `{B,C,D}`, single data source, data ingestion/distribution


## LF Job Creation and Scheduling Details

+ LF Task Config Options Major Categories
	1. Params & Dynamic Value Refs: Task/job level, adds flexibility
	2. Retries: Task/job level, first line of defense, different retry strategies
	3. Notification Alerts: Task/job level, granular target control

+ Task-Level Params:
	- JSON Arrays (Key-Value Pairs)
	- Supports: Conditional execs, looping, pass context between tasks

+ Job-Level Params:
	- Applied to all tasks
	- Overrides same-keyed task params