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


+ Ingestion Methods - Incremental/Normal Batch
	- Batch - CTAS (CREATE TABLE AS): can infer a unified schema, can be used with streaming-tables via autoloaders, `<CTAS> SELECT * FROM read_files(path,format,**);`
	- Incremental Batch - COPY INTO: idempotent, FORMAT_OPTIONS()=source-parsing/interpretation, COPY_OPTIONS()=`mergeSchema`(schema evolution), `force` (idempotency), `COPY INTO tbl FROM 'cloud_dir_path' ...`
	- AUTO LOADER:		 

+ Ingestion Methods - AutoLoader
	- Incremental batch or streaming ingestion: simple, scalable, relies on Spark Structured Streaming
	- Python: `spark.readStream.format("cloudFiles").**.load("vlm").writeStream.trigger(processingTime="5 seconds").toTable("ctlg.db.tbl")`
	- SQL (Declarative Pipelines): `CREATE OR REFRESH STREAMING TABLE tbl SCHEDULE EVERY 1 HOUR AS SELECT * FROM STREAM read_files()`