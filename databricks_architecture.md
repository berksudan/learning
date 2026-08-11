# Databricks Data Architect Learning Plan

## Databricks Data Intelligence Platform

+ Available for Data and Business Teams
+ 4 Core Pillars
	1. Lakeflow: Ingest, ETL, Streaming
	2. Databricks SQL: Data Warehousing
	3. AI/BI: Business Intelligence
	4. Mosaic AI

+ Supports: Iceberg, Delta Lake, Parquet

+ Simplified, open-source, 1 source of truth

## UC (Unity Catalog)

+ Foundation of the Intelligence Engine that simplifies the platform experience on every layer
+ Unified governance for all assets

+ Main Functions
	- Security: Access Control, Auditing
	- Collaboration: Discovery, Secured open data sharing 
	- Quality: Lineage, Quality Monitoring 
	- Insights: Cost Control, Business Semantics

+ All signals into UC feeds AI
+ Databricks gains awareness of your unique data and business context
	- Search: Find the right data/AI assets
	- Relevance: Highly relevant response
	- Secure: return only allowed data


## Lakeflow (3 Components): IncomingData

+ Lakeflow Connect: Connectors to key datasources (sql, streaming, salesforce, etc.)
+ Lakeflow DLT: Declarative Framework with Python/SQL, Reliable/Scalable data pipelines, Quality/Error Controls
+ Lakeflow Jobs: orchestration/automation of data pipelines for analytics and AI, monitoring, troubleshooting, observability

## Databricks SQL / Data Warehousing

+ Foundational Functionality + Governance/Administration
+ Automatic Tooling migrating from legacy DBs to SQL.

## AI/BI Business Intelligence

+ Scale BI: to everyone with low cost
+ Fast Results
+ Secure by Design: with Unity
+ AI/BI Genie: get responses/tables/visualizations in natural language

## Mosaic AI

+ Complete Agent Platform
+ GenAI based Applications
+ Supports: MLFlow, AutoML

+ DataPrep: ingestion, ML features, vector index
+ Agents reason across every enterprise ecosystem
+ Models: Supports all (existing/future) GenAI/ML Models
+ Governance: Guard Rails, Evaluation, Monitoring, rate-limits, usage tracking


## Lakehouse Architecture - Scope

+ Align with the Stakeholders on these 3 Areas
	- Architectural Components
	- Personas: served by the Lakehouse
	- Platform Domains: Applicable Domains/Use-Cases


+ Architectural Components
	- Functionality: Data Lake + Data Warehouse
	- Cross Team Colab
	- Faster Data Delivery + AI Insight

+ Personas: DataEngs, DataScientists, MLEngs, DW Admins, Data Analysts/Business Partners

+ Platform Domains and Use Cases: Governance, Storage, DW, Orchestration/ETL, Advanced Analytics/ML/GenAI, BI


## Databricks Data Intelligence Complete Architecture

+ Layer 5/4/3 - Collaboration: Delta Sharing, Marketplace, Clean Rooms
+ Layer 5
	- 5.1 Dev Tools: IDE Support, Notebooks, MLFlow
	- 5.2 BI: AI/BI Genie, AI/BI Dashboard, Unified SQL Editor
	- 5.3 Data/AI Apps: build/serve Databricks Apps
+ Layer 4 Automation: Lakeflow Jobs (Jobs, Declarative Pipelines), CI/CD, MLOps
+ Layer 3 - Apache Spark + Photon 
	- 3.1 Ingest & Transform: Batch/Streaming, Data Quality, Lakeflow Connect, Lakeflow Declarative ETL Pipelines & Autoloader
	- 3.2 Advanced Analytics, ML & AI: ML Modeling, GenAI, Real-time Analytics, Model Serving
	- 3.3 Data Warehouse: SQL, AI Funcs

+ Layer 2 - Data Intelligence Engine: Search/Discover, AI Assistant, Performance Optimization
+ Layer 1 - Data & AI Governance with UC: Access Control, Auditing, Lineage, Discovery, LH Federation, LH Monitoring
+ Layer 0 - Cloud Storage: Files (JSON, csv, images, ...) ➡️ Delta Lake ➡️ 3 Cloud Providers (AWS S3, Azure, GCP)


## Lakehouse 6 Guiding Principles

1. Data-as-Products: Curate data, be trusted
	- Clear definition, schema, lifecycle
	- Semantic Consistency
	- Medallion Structure: bronz (raw) - silver (curated) - gold (business-ready)
2. No Silos:
	- Remove data silos, minimize data movement
	- Avoid copies and outdated
3. Self-Service: Democratize Value Creation
	- Low Barrier to access data for everyone 
	- Lean Data Management
	- AI/BI Genie helps here
4. Org-wide Data Governance Strategy
	- Should be actively managed 
	- Access control, auditing, lineage
	- Use roles, columnar/row access controls
	- Databricks covers: Data Quality, Data Catalog, Data Access
5. Open Interfaces/Formats: encourage
	- Simplifies integration
	- Open up an ecosystem of partners
	- Cost is lower
6. Scale/Optimize: build to scale, optimize for cost/performance
	- Horizontal Scaling: more nodes
	- Vertical Scaling: increase size of nodes
	- Decouple data and compute resources


## Databricks <> Cloud Data Storages

+ Sources:
	- ETL: (Semi/Un)Structured Data
	- Federation (DWH, RDBMS, SaaS, Hive MS)
	- Sharing (Market Places / Data Shares)
+ Ingest:
	- Batch & Streaming: Auto Loader, Lakeflow Connect, Kafka
	- Ingest Tool, Event Streaming
+ Transform:
	- Lakeflow Declarative Pipelines
	- Spark
+ Query / Process
+ Serve
+ Analyse
+ Integrate
+ Storage


## Well Architected Lakehouse Frameworks

+ Operational Excellence:
	- Optimize Processes
	- Automation
	- Manage Capacity: limits, access limits
	- Monitoring: logging, alerting
+ Security, Compliance, Privacy:
	- Identity & Priveleges
	- Data Security
	- Network Security: Firewall
	- Compliance and Privacy
	- Secure Monitoring: Security scanning
+ Reliability:
	- Design for Failure: anticipate outages, design for resilience
	- Manage Data Quality: actively check, maintain trustworthiness of data
	- AutoScaling: can easily horizontal/vertical scaling, optimize cost
	- Recovery Procedures: Disaster recovery system
	- Automation: Simulate failures, recreate past failures 
	- Monitoring: Alerting, monitoring, logging
+ Performance Efficiency
	- Serverless Services: high availability, minimum config
	- Design for Performance: optimal performance
	- Performance Testing: continuous
	- Performance Monitoring: find bottlenecks/errors
+ Cost Optimization
	- Optimal Resources
	- Dynamic Allocation
	- Cost Monitoring
	- Workload Optimization
+ Data & AI Governance
	- Unify Data & AI Management
	- Unify Data & AI Security
	- Data Quality Standards: Completeness, Validity
+ Interoperability & Usability:
	- Integration Standards
	- Open Formats & Interfaces
	- Simplify building use cases
	- Consistency & Usability

## Data Architecture Strategies

+ Standardize in Data Storage & Governance
	- Secure & Compliant
	- Consistent & Predictable
	- Efficient Ops
	- Ready to build any data/AI product
	- Vendor interoperability, optionality, leverage
	- Own and store your data once
	- Future-proof, scalable, interoperability
+ Prioritize Use Cases
+ Democratize
	- Scalable
	- Offers as a product


## The Medallion Structure

+ Bronze: Raw Ingest
	- No transformation, append Only
	- Single Source of Truth
+ Silver: Cleansed/Conformed
	- Typed/deduplicated/joined 
	- Null Handled
	- 3NF / ERP
	- Raw/Data Vault
+ Gold: Consumption ready
	- Business Vaults + Marts (subject-focused subset of a data warehouse)
	- Aggregated, enriched
	- Materialized view, feature tables
	- Star Schema (Kimball): Fact/Dimension Tables


## Delta Lake & Unity Catalog Features

+ Delta Lake
	- ACID `MERGE INTO` for SCD2 and Satellite loads
	- `GENERATED ALWAYS AS IDENTITY` for surrogate keys
	- Informational `PRIMARY KEY` / `FOREIGN KEY` constraints
	- Time travel for audit and rollback

+ Unity Catalog
	- Three-level namespace: `catalog.schema.table`
	- ER diagram rendering from PK/FK constraints
	- Lineage across Bronze -> Silver -> Gold
	- Unified governance for tables, views, features, models


## Data Warehouse Overview

+ OLTP-Transactional
	- Purpose: Record business events
	- Queries: Few rows, indexed point lookups
	- Schema: Normalized (3NF)
	- Storage: Row-store
	- Consistency: Row-level, real-time
	- Users: Applications

+ OLAP-Analytical
	- Delta Lake is OLAP
	- Purpose: Analyze patterns + trends
	- Queries: Wide scans, aggregations
	- Schema: Dimensional, wide, or vault
	- Storage: Column-store (Parquet / Delta)
	- Consistency: Eventually consistent
	- Users: Analysts, BI, ML pipelines

+ Inmon - 4 Properties of DWH
	1. Subject-Oriented: Organized by Business Subject, in Delta: ACID transactions
	2. Integrated: 1 set of names, formats, keys, in Delta: `MERGE INTO`
	3. Time-Variant: History preserved, in Delta: time-travel
	4. Non-Volatile: Append + version, no in-place updates, in Delta: schema evolution


## The Three Classical Data Model Approaches

+ Often used in combination, not mutually exclusive
+ Common: Inmon Silver 3NF -> Kimball Gold

1. Inmon - Corporate Information Factory (CIF)
	- Top-down
	- Integrated 3NF enterprise model feeds dependent marts
	- Strengths: SSoT, Strong Integration
	- Weaknesses: Long lead time to value, Harder to change downstream

2. Kimball - Dimensional
	- Bottom-up
	- Star schemas built mart by mart, linked via conformed dimensions
	- Strengths: Fast to deliver, BI-friendly, intuitive
	- Weaknesses: Integration via conformed dims (cross-mart integration), Not audit-oriented

3. Data Vault 2.0
	- Hub / Link / Satellite:
	- Strengths: Full audit trail, Parallel-load friendly, Easy to extend
	- Weaknesses: More artifacts to manage, Needs Business Vault on top

+ How to Pick?
	- Heavy Audit? Yes: `Data Vault 2.0`
	- Many Volatile Source Systems? Yes: `Data Vault 2.0` 
	- BI First Stable Sources? Yes: `Kimball`, No: `Blend (Silver 3NF + Gold Star)` 


## Data Modeling Tiers: CDM, LDM, PDM

+ CDM (Conceptual Data Model): Owned by Business Stakeholders
	- Business View
	- Identifies core entities + relations without technical detail

+ LDM (Logical Data Model): Owned by Data Architects
	- Attribute View
	- Adds keys, data types, cardinality (1:N, N:M, 1:1) and normalization rules
	- Platform-independent - describes what without prescribing where

+ PDM (Physical Data Model): Owned by Data Engineers
	- Implementation View
	- Maps the logical model to Delta tables with `CREATE TABLE DDL`, `PK/FK constraints`, partitioning, identity cols


## Inmon - Corporate Information Factory (CIF)

+ Operational Sources --->  ODS (Operational Data Sources, near real-time)
+ Bronze (Stage)
+ Silver (Enterprise 3NF Warehouse)
+ Gold (Marts): Finance, Marketing, Ops

+ UNF: Unnormalised
	- Repeating Groups
	- Multi-valued Attributes (e.g Json Dict)
	- Redundant Rows 
+ 1NF: Atomic Values
	- 1 value per cell
	- No repeating groups
	- Each row unique
+ 2NF: No partial deps
	- Split composite tables
+ 3NF: No transitive deps
	- Non-keys depend only on PK

+ Deletion vectors: reduce the performance impact of normalization

+ ERM: The Language of the Warehouse
	- Entity: Table, must have NON-NULL PK, 
	- Attribute: Column, `NOT NULL` and `CHECK` enforced in write-time
	- Relationship: FK with Cardinality (1:1, 1:N, M:N), `NOT ENFORCED RELY` vs. `MERGE INTO` (we check referential integrity)

+ PK / FK Constraints
	- PK: `CONSTRAINT pk_custkey PRIMARY KEY (c_custkey)`
	- FK: `CONSTRAINT fk_custkey FOREIGN KEY (o_custkey) REFERENCES labuser.silver.lab_customer(c_custkey)`
	- Informational PK/FKs: document model intent, power ER diagrams in Catalog Explorer, and enable optimiser tricks like join elimination.
	- Enforcement is the pipeline's job, typically `MERGE INTO` with dedup.
	- `RELY` clause yields wrong results if data inconsistency

+ Use Inmon when:
	- Large enterprise, many sources: A 3NF silver is Cheaper
	- Stability > mart agility
	- Strong governance + audit: Clean Lineage

+ DON'T Use Inmon when:
	- Small team, fast delivery
	- BI-only use cases
	- Volatile Sources: Frequent schema changes disrupt 3NF

+ Databricks uses:
	- Common Mix: 3NF-Silver + Kimbell-Gold
	- Common for Silver: 3NF or Data Vault
	- Data Vault: Separates business keys (Hubs), relationships (Links), and descriptive attributes (Satellites)


## Kimball's Dimensional Modeling

+ Star Schema - Fact Table
	- Business event measurements
	- Size: Many rows, narrow
	- Joins: Surrogate Keys (not business keys)
	- Grains: What one row represents

+ Star Schema - Dimension Table
	- Denormalized
	- Descriptive context for a fact
	- Size: Fewer rows, wide
	- Surrogate PK + natural business key
	- SCD: Slowly Changing Dimensions, tracks attribute changes
	- Version Aware

+ 4 Fact Table Types
	1. Factless: An event occurrence record, no numeric measure
	2. Transactional: Event per row, most common, append-only, immutable
	3. Periodic: Period per Row, event(s) in a period 
	4. Accumulating: Process per Row, `UPDATE`s Columns, Only updated type, dedup is needed

+ Surrogate Keys:
	- On Delta Table: `GENERATED ALWAYS AS IDENTITY` for auto-surrogate-gen on `INSERT`
	- System-generate INT/identity column
	- Identifies a version of a dimension row
	- Changes with every difference in attributes
	- `BIGINT` join performance > `STR` or `composite key` 
	- Example: `dim_customer_key BIGINT GENERATED ALWAYS AS IDENTITY,`

+ SCD (Slowly Changing Dimensions)
	- Defined per Attribute
	- Type 0: No change, ignore changes
	- Type 1: Overwrite, e.g. typo fix, no history
	- Type 2 (SCD2): New row per change, needs _DEDUP_, Atomicity, close old + create new
	- Type 3: New column per change, keep `prev` + `curr`

+ SCD2 Merge Steps
	1. Attribute in Source changed
	2. EMIT: OLD row + NEW row into STAGING
	3. UPDATE OLD row: close it, `is_current` = `False`, `end_date = XYZ`
	4. INSERT NEW row:  Surrogate Key (`is_current` = `True`)

+ MERGE INTO Clause Reference:
	- `WHEN MATCHED` UPDATE/DELETE old version
	- `WHEN NOT MATCHED` INSERT new version
	- `WHEN NOT MATCHED BY SOURCE`: UPDATE/DELETE, expire target dimension when source disappears
	- DEDUP requirement: runtimeError if dups in source

+ Snowflake Schema
	- USE ONLY WHEN: hierarchy semantics genuinely matter
	- Hierarchies normalized into their own tables
	- Multiple Hops: Hierarchies are separate tables
	- More joins Required: for BI queries that need the full hierarchy
	- Preserves Semantic Meaning: of each level
	- Less Redundant Storage: since hierarchy values are stored once

+ Star vs Snowflake Schema
	- Snowflake: slower, complex joins, more hops, less data
	- Star: can use columnar (e.g. Parquet), broadcast joins
	- Delta favors STAR due to denormalisation tolerance

+ Optimizing FactSales on Delta
	- Data skipping: get min/max stats, skip irrelevant range in filters
	- Z-ORDER: colocate row with similar values. Run `OPTIMIZE` after bulk loads or on a schedule
	- Liquid Clustering: Cluster keys at table creation, better than Z-order, recommended for most common filter keys


## Data Vault 2.0 - Hubs, Links, Satellites

+ In Short: Auditable, Scalable, Hash-Keyed Warehouse Modeling

+ Separates Structures (business keys & relationships) from Context (descriptive attributes)

+ Main Features
	- Mandatory Audit: Full History, No Overwrite
	- Volatile Sources: schema changes, late arrivals
	- Parallel Teams: Independent domain loads, no coordination, uses MD5 Hash Keysaudit need
	- Complex and steep learning curve

+ Compared to Inmon and Kimball
	- Inmon is poor at Auditing: Adding a new source can rewrite histor/tables
	- Kimball is poor at Parallelization: SCD2 strict dependency order

+ 3 Core Artifacts - Hub
	- In Short: business keys
	- Registers an entity existence
	- 1 hub per Business Concept
	- 1 row per Business Entity
	- Never stores descriptive attributes
	- Mandatory Cols: `hash_key` (PK), `business_key`, `load_ts`, `record_source`

+ 3 Core Artifacts - Link
	- In Short: relationships
	- Insert-Only
	- 1 Row per Unique Combination of parent `hash_key`s
	- Captures that 2≥ Hubs are related
	- Holds: 1 FK column per participating Hub
	- Mandatory Cols: `composite_hash_key` (PK), `parent_hash_keys`, `load_ts`, `record_source`

+ 3 Core Artifacts - Satellite
	- 1 Satellite per Source per Context
	- In Short: descriptive + history
	- Attribute of a Hub or Link
	- Insert-only: a new row is added each time attributes change, preserves history
	- New Source = Add Satellite (no hub/link)
	- Mandatory Cols: parent `hash_key` (FK), `hash_diff`, descriptive attributes, `load_ts` + `record_source`

+ Hash Keys and Load Pattern
	- Derived: All Hashes are derived (from input), not generated
	- Parallel Load: H/L/S can load hash-keys in parallel and in any order
	- MD5 Hashing: `hash_md5(any input)` <-> `32-char hex`, unique 1-1, no output collision
	- `hash_key`: business-key(s) only, CANNOT change, used in hubs (PK), links (composite PK), Satellites (FK)
	- `hash_diff`: Descriptive attributes only, CAN change, used in Satellites only

+ Using Hashes:
	- Multi Column Hash: `hash(val1||val2||val3)`, `||` is needed for collisions
	- For Null: `COALESCE(col, 'NULL_SENTINEL')`

+ Satellite Hash Diff Comparison
	- MATCH with the new record: Skip (no-op)
	- DIFFER with the new records: Create a new row

+ Medallion Architecture in Data Vault 2.0
	- Raw Vault (Silver): Audit Layer, H/L/S live here in parallel
	- Business Vault (Silver): Point-in-Time (PIT) tables, bridge tables, computed Satellites for derived metrics
	- Information Marts (Gold): BI-ready data, common to use Star schemas (Dim=Hub+Satellites, Fact=Link+Satellites) or flat UNF views

+ Choose Data Vault when:
	+ Regulated; finance, health, gov
	+ Many Volatile Sources
	+ Parallel teams per domain
	+ "What did we know, when?" queries: Satellite History + Delta Lake Time Travel

+ DON'T Choose Data Vault when:
	+ Small team, single source
	+ BI-only with no audit need
	+ No need for history

## Modern Gold-Layer Pillar #1 - Feature Stores (ML)

+ Training/Serving Skew Problem (Without ML Feature Store):
	- When same features are not available in training and inference
	- Feature logic re-implemented in notebooks, training jobs, and serving endpoints
	- Subtle drift between training and serving
	- No shared discovery across teams
	- Solution: Define feature once, serve to both

+ ML Feature Store
	- One definition feeds training, batch, and real-time
	- Training = serving by construction
	- Unity Catalog: Features governed as first-class assets
	- Discoverable and usable across teams 

+ Databricks Implementation
	- Use `FeatureEngineeringClient.create_table()` w/ `timestamp_keys` or `register_table()`
	- `log_model()` so it records the feature lookups as model metadata (fresh keys)

+ Use Feature Store When:
	- Multiple models reuse the same derived data
	- Real-time inference at low latency
	- Training/serving parity must be auditable
	- Cross-team feature discovery is a priority
	
+ DON'T Use Feature Store When (Gold Table is enough):
	- Single Daily Batch Model
	- No real-time serving requirement
	- No cross-team use

## Modern Gold-Layer Pillar #2 - Metric Views (Analytics/BI)

+ Define Metric View Once in Unity Catalog (Governed)
+ Sits between Gold Table and Consumers
+ Single Source of Truth: Let Dashboards, Notebooks, Genie Space use the same definition
+ Can be versioned (via UC)

+ Metric View YAML Definition:
	- Source: Gold table, a lineage pointer
	- Filters: Optional but not overridable row filter
	- Dimensions: Valid slices incl. derived expressions
	- Measure: Named aggregate expressions
	- Composability: One metric view can use measure from another metric view
	- Materialization: Supported and refreshable

+ Measure Types
	- Additive Measures: can be summed across any dimension without limitations
	- Descriptive Measures

+ Use Metric View when:
	- Multiple dashboards report the same KPI
	- Business users query metrics via Genie
	- Metric definitions need to be versioned and governed
	- Finance or compliance requires consistent metric calculation

+ DON'T Use Metric View when (Gold View or Table suffice):
	- Ad-hoc analysis, not a recurring KPI
	- 1 dashboard, 1 author
	- Metric definition is not shared across teams

## Modern Gold-Layer Pillar #3 - Delta Sharing (Collaboration)

+ A single Gold table can feed all three pillars simultaneously

+ Without Delta Sharing
	- Export to file
	- Stale data
	- No access control after export
	- No lineage or audit trail

+ SQL Notation
	- `CREATE SHARE shr;`
	- `ALTER SHARE shr ADD TABLE tbl;`
	- `CREATE RECIPIENT ext_corp;`
	- `GRANT SELECT ON SHARE shr TO RECIPIENT ext_corp;`

+ ALTER SHARE Options
	- `WITH HISTORY`: share full delta log, enables time travel and streaming reads
	- `PARTITION (col = value)` + `AS alias`
	- `ADD SCHEMA schema_name`: share the existing/future `catalog.schema.*`

+ Databricks-to-Databricks Sharing: 
	- Mounting: Recipient mounts the share as read-only
	- Recipient uses their metadata ID in the format `cloud:region:uuid`
	- No Credential Files needed

+ Use Delta Sharing when:
	- External partners need access to curated data
	- Internal teams across different metastores need shared tables
	- Regulatory reporting requires controlled, auditable access
	- Data products need to be published for broad consumption

+ DON'T Use Delta Sharing when:
	- All consumers are in the same Unity Catalog metastore 
	- Standard grants and views provide sufficient access control
	- No cross-organization sharing requirement
	- Standard `GRANT` is enough


## Combining Data Modeling Approaches

+ Blend Inmon, Kimball and Data Vault on the Lakehouse

+ Blending Is Normal

+ Industry Starting Points
	- Retail and consumer goods: Kimbell
	- Financial services and insurance: Data Vault Silver
	- Healthcare: Data Vault Satellites

+ Popular Choice Flow:
	- Source Systems
	- BRONZE: Raw Capture
	- SILVER = `Inmon (3NF)`, GOLD = `Star Schemas (Kimbell)` OR
	- SILVER = `Data Vault (Raw Vault)`, GOLD = `Business Vault` + `Star Schemas (Kimbell)`
	- Serve: Feature Store (ML), Metric View (BI), Delta Share (Collab)

+ 3 Common Patterns
	1. 3NF (Silver) → Kimbell (Gold): Enterprise integrations + Good BI, _BAD_: high modeling effort, latency
	2. Data Vault (Silver) → Kimball (Gold):, Regulated, multi-source, or audit-heavy environments, _BAD_: more artifacts to build/maintain
	3. 3NF + Data Vault (Silver): Large org where different domains have different needs, _BAD_: Teams must agree on naming/governance conventions

+ Choosing a Blend
	- Small, stable, well-understood domain?: Pattern 1
	- Is enterprise-wide integration the priority?: Pattern 1
	- Regulated, multi-source, or audit-heavy?: Pattern 2
	- Do source systems change frequently?: Pattern 2
	- Are some domains simple while others are complex?: Pattern 3
	- Do different teams need different levels of history and auditability?: Pattern 3
	- Is fast BI delivery more important than integration?: No Silver, directly Kimbell Gold


## Defining Data Products

+ Gap Between a Well-Modeled Table and a Usable Product
	- Organizational, not technical
	- Without answers, analysts make mistakes

+ Domains Publishing into Unity Catalog
	- UC is single enforcement point: 1 permission model, 1 audit log, 1 lineage graph
	- Domains -> UC -> BI Analysts, Data Scientists, Apps / APIs
	- Catalog Explorer surfaces owner, tags, lineage, and comments alongside the table.

+ Central Warehouse: bad practice
	- Central team owns all data
	- 1 model fits all
	- Pipelines = plumbing:
	- Governance applied later

+ Data Mesh: good practice
	- Scalable organization model
	- Domain teams own their data
	- Domain-specific models with conformed interfaces
	- Pipelines = part of the product
	- Governance from day one 
	- Start Small: 1 domain -> 1 table -> add ownership, SLA, docs, lineage -> Expand

+ DATSIS (What Makes a Dataset a Data Product) 
	- Discoverable: Listed and searchable
	- Addressable: Stable URN or path
	- Trustworthy: SLAs, quality, lineage
	- Self-describing: Schema, docs, samples
	- Interoperability: Conformed keys
	- Secure: Single access plane

+ DATSIS in Databricks
	- Discoverable: tags, Catalog Explorer search, AI-generated descriptions
	- Addressable: `catalog.schema.table` namespace that works identically in SQL, Python, Jobs, Delta Sharing
	- Trustworthy: lineage tracking, pipeline expectations, Delta time travel, system table audit logs
	- Self-describing `COMMENT ON TABLE`, `COMMENT ON COLUMN`
	- Interoperability: PK/FK constraints and Delta Sharing
	- Secure: UC's unified grant model with row filters and column masks enforced across all compute engines

+ 3 Catalog Explorer Monitor Types:
	- Snapshot (no timestamp column required)
	- Time series (tracks distributions per time window)
	- Inference (tracks ML model performance).

