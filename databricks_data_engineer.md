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
	- Scheduled: Cron, time-based processing, Timezone aware
	- Manual: On-demand, ad-hoc, can be run via UI/API/CLI/SDK/DABS, can be combined with other trigger types
	- File-Arrival: Event-driven, supports pattern matching, supports AWS-S3/AzureStorage/GCP-GCS/Dbx-Volumes
	- Table Update: Data change events (insert, update, del, merge). can set `min time between consecutive triggers`, can set `wait after last change` (delay job exec untill all source tables updated)
	- Continuous: Streaming workload, built-in retry logic managed by Dbx, good for real-time analytics, fraud-detection, IoT processing

+ LF Job Compute Options
	- Interactive / All-Purpose Clusters: shared, multi-user, expensive, no-prod, best for ad-hoc analysis / data-exploration / development
	- Job Clusters: High start-up time, 50% cheaper, lifetime bound to job, prod-grade, subject to cloud provider start-up times, can be reused across tasks
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


## LF Job Creation and Scheduling Details - Params, Notification, Retry

+ LF Task Config Options Major Categories
	1. Params & Dynamic Value Refs: Task/job level, adds flexibility
	2. Retries: Task/job level, first line of defense, different retry strategies
	3. Notification Alerts: Task/job level, granular target control

+ Task Params:
	- JSON Arrays (Key-Value Pairs)
	- Conditional Exec Support: Data condition branching, env settings, business rules
	- Looping Support: iteration counts, for-each loop arrays, complex processing
	- Context Passing: Data flow for downstream tasks

+ Job Params:
	- Applied to all tasks automatically
	- Overrides same-keyed task params
	- Can be overriden at runtime on job run trigger

+ Access Params in Task: `dbutils.widgets.get("parameter_name")`

+ Task Values - Dynamically Set/Get Task Params
	- Computed at Runtime
	- Dynamic Communications between tasks
	- Good For: share computed/dynamic results, conditional logic, processing stats for monitoring 
	- Set TaskValues: `dbutils.jobs.taskValues.set(key="a_key", value="val")`
	- Get TaskValues from another upstream task: `dbutils.jobs.taskValues.get(taskKey="task-name",key="a_key")`

+ Dynamic Value References Intro
	- Reference values at runtime
	- Notation: `{{ }}`

+ Dynamic Value References - Job Context References:
	- `{{job.start_time.day}}`: Get exec time
	- `{{job.run_id}}`, `{{job.parameters.environment}}`: Get job-level params

+ Dynamic Value References - Task Context References:
	- `{{task.name}}`
	- `{{task.retry_count}}`

+ Dynamic Value References - Inter-Task Communication:
	- `{{tasks.data-validation.values.record_count}}`: Get computed results from upstream tasks
	- `{{tasks.file-processor.values.output_path}}`: Get dynamic filepaths from other tasks

+ Notification Alerts
	- Job-Level Notifications: Customizable, On job completion
	- Task-Level Notifications: Customizable, On task completion
	- Targets: Email, teams, pagerDuty, Slack, Webhook
	- Per-Task Customization
	- Trigger Conditions - Lifecycle: job start, job complete with fail/success
	- Trigger Conditions - Late jobs: Timeout warning
	- Trigger Conditions - Streaming Backlog: Detect delayed streaming workloads
	- Trigger Conditions - Webhook: Custom conditions, API integration

+ Retry Policy
	- Defines: Conditions and how many times you retry
	- You should consider: failure type, resource impact, downstream dependencies, business SLA

## LF Job Creation and Scheduling Details - Conditional and Iterative Tasks

+ Run-if Conditional Task Dependencies
	- Control: Based on upstream task outputs
	- Handles: Partial Failure
	- Handles: Complex Dependency Scenarios
	- Dependency Conditions: all-succeeded, all-failed, 0-failed, 1+-succeeded, etc.
	- Configure via UI: Configuration Settings


+ If/Else Tasks
	- Boolean conditional logic
	- Uses boolean operators: `==`, `!=`, `>`, `>=`, `<`, `<=`
	- Example Conditions: Data conditions, param values, processing results, business rules, etc.
	- Business Logic Examples: Data Quality Gates, Processing Volume Decisions, Environment-Specific Logic, Business Rule Implementation

+ For Each Tasks
	- Iterative Processing
	- Input Array: Loops over an input array
	- Concurrency: Configurable, parallel iteration run with performance optimization
	- Dependency Management: Downstream tasks depend on the entire for-each container
	- Resource Management: The container allocates resources across iterations, optimizing cluster utilization and preventing resource conflicts.
	- For-each Task Type: Top-level container, defining input-array, concurrency, resource-alloc, 
	- Nested Task Type: Takes array-item as `{{ input }}` and executed


## Handling Task Failures and Monitoring Jobs Performance

+ Repair Feature with Rerun
	- Repair run reruns: The failed task & all its dependent downstream tasks
	- Targeted Recovery: Select the minimum unit
	- Parameter Override Capability: adjust resources, change processing logic, etc.
	- Cost Efficiency: Reduces cost/time/resources
	- In case of Task Failure: (1) modify the task & rerun, (2) modify the params & rerun

+ Repair Run Operational Benefits
	- Resource Optimization: low recovery time, saves money/time
	- Reduced Risk: no cascading failures
	- Faster Resolution: Fails-fast, improves SLA adherence and responsiveness

+ After Repair Run
	- Audit Trail: num-attempts, fixer person, time of fix,  
	- Success Validation: Clear indication of which tasks were recovered successfully, enabling confidence in the repair process
	- Learning Opportunities: Diagnose, improve, prevent

+ Monitoring Jobs Performance with System Tables
	- `system.lakeflow`: Built-in Catalog, logs all job activities across workspaces in region
	- Timeline Tables: Timeline analysis, uses `period_{start,end}_time` for long running job's hourly duration

+ Dashboards
  - Before use, the dashboard must be published and connected to a SQL warehouse


## Spark Declarative Pipelines Overview

+ Problem of Building Reliable Data Pipelines:
	- Labor-Intensive Development
	- Operational Complexity
	- Siloed Batch & Streaming
	- Solution: Spark Declarative Pipelines

+ Spark Declarative Pipelines Advantages
	- Simplified Pipeline Authoring: SQL/PY support, no orchestration logic (managed by LF), 0 boilerplate (built-in error handling & dep mgmt)
	- Intelligent Optimization at Scale: Auto-scaling (as data volumes grow), self-healing, ⬇️ overhead (⬆️ reliability, ⬇️ operational cost)
	- Unified Batch and Streaming: process historich/realtime data, adaptive performance/cost, same code for batch/streaming
	- Supports incremental load

+ Creating a Spark Declarative Pipeline
	- Workspace Menu: `Options (⋮) Button` -> `Create` -> `ETL Pipeline`
	- Jobs & Pipelines: `Create` -> `ETL Pipeline`



## SDP (Spark Declarative Pipelines) - Dataset Types

+ ST (Streaming Tables)
	- Process new data only, file names read once
	- Support for streaming/incremental data processing
	- Incremental Data Processing Mode: Supports batch/streaming
	- Efficient Data Updates: On each refresh, added data in the source tables are fetched.
	- SQL Command Usage: `CREATE OR REFRESH STREAMING TABLE`
	- Streaming Read Syntax with Checkpointing: `FROM STREAM read_files()` or `FROM STREAM src_streaming_tbl`
	- AutoLoader Integration

+ MV (Materialized Views)
	- Records are processed as required
	- Returns accurate results for the current data state
	- Used in Data Processings Tasks: Transforms, Aggs, pre-computed slow queries, frequently used computations
	- Dynamic Query Recalculation: On each MV update, query results are recalculated
	- Pipeline-Driven Maintenance: auto created/updated by the pipeline
	- SQL Command Usage: `CREATE OR REFRESH MATERIALIZED VIEW`
	- Flexible Pipeline Placement: Use anywhere in the pipeline
	- Incremental Result Refresh: On Serverless compute if applicable
	- Cost-Based Optimization: Fast/efficient transforms on Serverless compute
	- Unlike streaming tables, materialized views automatically track changes and manage their own refreshes based on the upstream source
	- No `STREAM` Keyword: in `FROM` clause

+ View Overview & Limitations:
	- Virtual table/query with no physical data
	- No `OR REFRESH` Clause in SQL
	- UC Pipeline: Mandatory type
	- No Streaming Queries: Can be in views
	- Cannot be Streaming Source: For a Pipeline 

+ Temporary View
	- Pipeline-Scoped: No UC entry
	- SQL-Based Intermediate Layer: `CREATE TEMPORARY VIEW`

+ View:
	- SQL: `CREATE VIEW`
	- UC Entry

+ DLT (Delta Live Tables) to SDP: DLT is deprecated

+ The Declarative Pipeline Graph: automatic pipeline dependency parsing


## SDP (Spark Declarative Pipelines) - Data Quality with Expectations

+ Expectations
	- Row-by-row data quality rules
	- Materialized Views with Expectations: Fully refreshed during pipeline runs
	- SQL: `CONSTRAINT constraint_name EXPECT (column_condition) [ON VIOLATION action]`

+ `WARN` Violation Action
	- Default behavior on no action
	- Log Violations: incl. valid/invalid record counts and other metrics
	- Keep Invalid Rows: still written to target
	- SQL:  `CONSTRAINT valid_notification EXPECT (notifications IN ('Y','N'))`

+ `DROP` Violation Action
	- Drop invalid Rows on violation
	- Log Dropped Rows Counts: with other metrics
	- SQL: `CONSTRAINT valid_date EXPECT ( data > "2025-01-01 ) ON VIOLATION DROP ROW`

+ `FAIL` Violation Action
	- On Violation: fail specific flow
	- Manual Intervention: Required
	- SQL: `CONSTRAINT valid_id EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE`

+ Full SQL Example with Constraints
	- `CREATE OR REFRESH STREAMING TABLE tbl`
	- `(CONSTRAINT <CSTRT_STMT>, CONSTRAINT <CSTRT_STMT>)`
	- `AS SELECT <SELECT_STMT>`
	- `FROM STREAM another_tbl`