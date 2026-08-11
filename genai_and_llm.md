## Generative AI and Agents in Databricks - Basics 

+ Trace Based Debugging:
	- Span: single unit of step/work in a GenAI Flow
	- Contains: tools-called, prompts, inputs, outputs, Vector-search
	- Databricks supports `OpenTelemetry`
	- Agent Bricks Custom Agents

+ LLM-as-Judge
	- Can be finetuned by human input
	- Databricks: `JudgeBuilder`
	- MLFLow supports this

+ Monitoring Agents
	- Data Quality Monitoring: Anomaly Detection, Data Profiling
	- Integrates with Databricks SQL Alerts and Dashboards

+ Agent Bricks
	- Information Extraction: summarize, translate, flexible
	- Knowledge Assistant: Advanced Grounding with Instructed Retrieval, works with UC/MLFlow
	- Supervisor Agent: Advanced orchestration of subagents, routes to subagents
	- ALHF (Agent Learning on Human Feedback)

## Prompt Engineering

+ PromptEng Definition
	- Practice of optimizing input (prompt) to optimize the LLM output
	- Tactical Discipline on the instruction layer

+ PromptEng Techniques:
	-	Few-Shot Prompting (providing examples)
	- Persona Adoption (assigning a role)

+ Non-Reasoning Models (e.g., Llama 3, GPT-4o)
	- Statistically Predict the next token
	- You need to prompt `Chain of Thought (CoT)`, e.g. "Think step-by-step"

+ Reasoning Models (e.g., OpenAI o1)
	- Generate an internal `CoT` before answer
	- Focuses goals and constraints, not thinking

+ The Boundaries of Prompting
	- Knowledge Cutoff: training data is until last year
	- Hallucination: plausability over truth
	- Ambiguity: without private context, gives generic interpretations

## RAG (Retrieval Augmented Generation)

+ Retrieval Agent: Agent working with RAG

+ Key Stages
	- Retrieval: search a KB for chunks (indexed via Mosaic AI Vector Search)
	- Augmentation: Inject chunks to Context Window
	- Generation: Synthesize _using_ only injected data

+ Context Rot causes
	- Confused model with too many chunks
	- Context Poisoning: conflicting/irrelevant info
	- **Lost in the Middle:** in long CW, model favors first-last data

## Context Engineering

+ Context Environment: Entire Input Window
	- System Instructions
	- Conversation History 
	- Retrieved Data
	- User Constraints

+ Designing System Prompts
	- Role Definition: persona
	- Negative Constraints: don't do this/that
	- Output Formatting: structured output for interoperability

+ Strict Grounding and Chunking
	- Grounding Instructions:
	- Metadata Filtering: Use UC metadata to filter retrieval

+ Managing Multi-Turn State
	- Summarization: Compress convo history
	- Moving Window: discard old messages
	- Selective Persistence: determine the permanent vs. state context in CW.

+ CW (Context Window)
	- Has Input Tokens: prompts/instructions, history, retrieved data
	- Has Output Tokens
	- IF filled: high latency, bad reasoning (lost in the middle)

+ Token Economics Optimization
	- Just-in-Time Retrieval: retrieve only needed
	- Reranking: 50 chunks -> 5 Chunks -> CW


## Data Storage, Processing, Cleaning Architecture

+ UC Volumes (Bronze): Governance Layer for non-tabular/raw data, lineage

+ Delta Lake (Silver/Gold): stores parsed/chunk data, ACID, versioning

+ Data Ingestion and Processing Workflow:
	- Data Ingestion and Pre-Processing: read from UC volume, parse via AI func
	- Data Storage: Store parsed data in Delta Lake with Governance
	- Chunking: Split data for embedding generation

+ Doc Processing Challenges:
	- Hierarchical Info: headers/subheaders
	- Order Preservation: multi-col text
	- Contextual Integrity: images/charts/photos must be associated with text descriptions

+ OCR (Optical Character Recognition) or LLMs: Good for parsing

+ Parse/Process Doc with AI Func `ai_parse_document` in Databricks
	- Serverless run
	- Scalable
	- Unstructured -> Structured JSON (VARIANT)
	- Layout Awareness
	- Figure Descriptions: text desc from charts/images
	- Bounding Boxes: returns coordinates (bboxes) for text elements
	- Image Path Param: `imageOutputPath`

+ Parsed Data contains:
	- Metadata
	- Parsed Content
	- Pages
	- Error_status
	- Corrupted data

+ Data Cleaning and Transformation
	- Noise Reduction: remove artifacts, headers, footers
	- Metadata Injection: document titles, author names, creation dates


## Chunking Strategies

+ Fixed-Size Chunking (Legacy/Baseline):
	- Hard character/token limit
	- Cut in Half Problem

+ Recursive Chunking (Standard)
	- Uses: sentences, paragraphs, sections
	- Often Injects: relevant metadata, tags, titles

+ Chunk Overlap
	- 10-20% Overlap
	- Prevents sentences or ideas from being cut off abruptly

+ Embedding-Based Semantic Chunking
	- Break a Chunk when Semantic/Embedding discrepancy between sentences
	- Example: Topic Change

+ Windowed Summarization
	- Retain current chunk + Summary of Previous chunk(s)

+ Embedding Model Considerations
	- CW Limits of Embedding Models: lost/incomplete data due to truncation beyond the limit, lost-in-the-middle
	- Granularity vs. Context: large chunk = diluting context, small chunk = precise without surrounding context

+ Tools and Frameworks for Chunking
	- Parsing (Extraction): `ai_parse_document` in Databricks
	- Conversion from JSON to MD: `ai_query` (LLM, expensive), manual (cheap)
	- Chunking (Splitting): LangChain or Custom Functions (UDFs)


## Embedding and Vector Search

+ Core Concepts of Embeddings
	- Embeddings: Numerical representation of content, preserves semantics
	- Multimodal Context: support for image, video, audio
	- Embedding Models

+ Embedding Models 
	- ML/DL Models
	- Converts: High-dimensional unstructured data -> Low-dimensional numerical vectors
	- Similar semantics = Close vectors
	- Embedding Alignment and Comparability: Use the same embedding model for indexing docs and processing queries

+ Embedding Models - Key Factors to Choose
	- Vocabulary Size and Domain: Was training data generic or domain-specific?
	- Context Window: Maximum Input Token Limit, beyond is truncated/ignored
	- Vector Dimensions: High Dimensions are costly + more accurate + slower

+ Vector DB
	- Supports: CRUD
	- Excels: at similarity search
	- Specialized indexing structures
	- Optimized Vector Operations

+ Vector Search Methods
	- Similarity Search: Semantic correlation
	- Full-Text Search: Traditional keyword-based, excels at specific terms (part no, codes)
	- Hybrid Search: Mix of Similary + Full-Text Search, usually performs best 

+ Distance and Similarity Metrics
	- L1 (Manhattan Distance): abs difference in all dimensions, useful for clustering and anomaly detection
	- L2 (Euclidean Distance): each axis is equally important, useful for grid-based or sparse data
	- Cosine Similarity: score ~ similarity, robust to magnitude/scale, most popular

+ Search Strategy - KNN (K-Nearest Neighbors):
	- Expensive
	- 1 Query <> All Data Points

+ Approximate Nearest Neighbors (ANN):
	- Cheaper
	- 1 Query <> Subset of Vectors
	- Advanced Indexing: HNSW (Hierarchical Navigable Small Worlds) or FAISS (Facebook AI Similarity Search) 

+ Reranking Process
	- Post-retrieval refining
	- Bridges: Precision gap in initial retrieval
	- Better Response Quality and Relavance
	- Less Hallucinations
	- Steps: Initial Retrieval (via fast ANN) -> Reranking (via Cross-Encoder) -> Reordering
	- Trade-offs: high latency, high cost, high computational overhead

## Mosaic AI Vector Search Engine (Indexer + Vector DB)

+ Native to Databricks Lakehouse

+ Enables Real-time similarity search through a REST API and Python client

+ Delta Auto Sync and Indexing: Source DeltaTable <> Vector Search Engine

+ Governance and Access Control: Unity Catalog at the index level

+ Narrow Down Search: Use Filters and Metadata.

+ Management and Ingestion Modes
	1. Managed Embeddings (Delta Sync): you only provide DeltaTable with raw text, uses _Mosaic AI Model Serving_ endpoint 
	2. Self-Managed Embeddings (Delta Sync): You compute embeddings and put in a DeltaTable, rest is Auto-sync
	3. Direct Access CRUD API: Ideal for real-time apps, used through REST API / Python SDK

+ Vector Search Requires CDF (Change Data Feed) enabled


## MLflow and Agent Development

+ MLflow Components (TTMM)
	- Tracking: API/UI for logging params, output files, metrics, code versions, tracking system prompts, retriever configs 
	- Tracing: Hierarchical execution flow of an agent
	- Models: Standard model packaging format
	- Model Registry: Centralized repo for lifecycle management, versioning, stage transitions

+ Experiments and Runs save:
	- System Prompts: for agent persona
	- Model Configs: params like `temperature`, `max_tokens`
	- Retriever Settings: `chunks to retrieve (k)`, `filtering threshold`
	- In Code: `mlflow.set_experiment()` on Workspace

+ Model Flavors and Wrappers
	- Model Flavor: integration to save/load/deploy a winning model
	- Native GenAI Flavors: `mlflow.langchain` or `mlflow.openai`, they handle serialization of retrieval chain and components
	- PyFunc Flavor: Wrap arbitrary code as model, good for custom re-ranking/dynamic-filtering, contains `.predict()`


## Observability, Tracing, and Governance

+ MLFlow Tracing: record every input, output, tool-calls, execution-graph 
+ Auto-Logging: e.g. `mlflow.langchain.autolog()`
+ Manual Instrumentation with `@mlflow.trace` decorator

+ Retrieval Failures
	- Empty/Irrelevant Retrieval: inspect Retriever Span
	- Vector Search Latency: check span duration
	- Hallucination despite Context:

+ Governance with UC - UC Model Registery
	- Access Control: Permissions for models/assets
	- Lineage: used data tables for the agent 

+ Governance with UC - Logging and Registering Agents
	- **Define Model Signature**: in/out format of model, use `mlflow.models.ModelSignature`
	- **Log the Model**: You can use `mlflow.{flavor, e.g langchain}.log_model`, better to add _Input Example_ to test
	- **Register**: Log to an experiment and run `mlflow.register_model("runs:/<run_id>/model", "catalog.schema.retrieval_agent")`
	- **Retrieval Tool in UC**: Should also be _governed_ 


## Knowledge Assistant with Agent Bricks

+ The Challenge of Production AI
	- Optimization Complexity: hard to find the optimal combination
	- Evaluation Difficulty
	- Cost vs. Quality Trade-off:

+ ALHF (Agent Learning from Human Feedback) Loop
	- 0. Declare Task: User defined data & intent
	- 1. Deploys: A baseline fast, Auto-provision Endpoint
	- 2. Collects: Feedback via Review App (👍, 👎, corrected answers) & LLM-as-Judge
	- 3. Synthesizes: Optimize prompts/configs

+ Bricks:
	- Pre-configured architectures
	- Specialized for a specific mode and data processing

+ Agent Bricks Use Cases
	- Knowledge Assistant: RAG, parsing, chunking, embedding, citation generation
	- Information Extraction: unstructured (img, pdf, txt) to structured (delta table)
	- Multi-Agent Supervisor: Query Router to Subagents 
	- Custom LLM: Creates a specialized LLM endpoint tailored to specific enterprise guidelines /tasks.

+ Code-First (Mosaic AI Agent Framework)
	- Maximum Control/Customizability
	- High Effort
	- High Code Update/Maintaining Cost
	- **Core Logic:** LangChain, LlamaIndex, OpenAI SDK
	- **Scaffolding, Tracing, Governance**: Mosaic AI Agent Framework

+ Declarative (Agent Bricks)
	- Outcome-oriented
	- Say _what to do_, not _how to do_
	- Fast delivery
	- Less control

+ Knowledge Assistant Components
	1. Data Ingestion and Parsing: use `ai_parse_document`, UC Volumes (pdf,txt,img) -> structured
	2. Mosaic AI Vector Search: managed/sync embeddings
	3. Reasoning Engine and Model Serving: query inference, citations
	4. Quality Loop (Review App & Evaluation): Review App, LLM Judges, Optimizations


## Issues in GenAI Applications

+ Select LLMs with:
	- High-quality/relavant training data
	- Relavant published benchmark (for your task)

+ Contextual Data
	- Implement Quality Controls
	- Monitor Changes

+ Model Input/Output
	- Collect/review input/outputs 
	- Monitor changes in stats
	- Monitor user feedback
	- Use LLM-as-judge metrics to assess quality

+ Bias/Ethics Issue
	- LLM Training Data: Private/sensitive, Biased
	- Contextual Data: Biased, unethical, illegal, unlicensed
	- Model Input/Output: harmful user behavior, harmful system responses

+ Data Legality Issue
	- Data Owner
	- Use for commercial/profitable purposes
	- Deployed app location

+ Harmful User Behavior (Prompt Injection) Issue
	- Extracts private info
	- Generates harmful/incorrect responses

+ Hard Solutions to the Issues (TQBS): Truth, Quality, Bias, Security

+ Implementing Guardrails
	- System prompt saying `never do that`
	- AI Playground Safety Filter Toggle in Databricks

## AI System Security

+ Top Concerns in AI:
	1. Security
	2. Cost
	3. Reliability

+ AISec is challenging, because
	- DataScience people are new to Sec
	- Sec teams are new to AI
	- MLEngs are new to complex models
	- Production introduces new real-time challenges

+ Secure each AI component to secure the system

+ DASF (Data and AI Security Framework) - Focused 6 Components
	- Data Catalog and Governance: Access control for data assets/models
	- Algorithms: Models, addresses data poisoning attacks
	- Evaluation: assess system performance and security issues
	- Model Management: access to models, move models into prod
	- Operations: ongoing quality and security through monitoring in prod
	- Platform Security: your whole platform

+ DASF (Data and AI Security Framework) - Other 6 Components
	- Raw Data
	- Data Prep
	- Datasets
	- Models
	- Model Prompting & RAG & Inference Layer
	- Model Serving

+ Mosaic AI Security Measures
	- Guardrails: Safety Filter, Llama Guard
	- Model Serving: Scalable/secure inference
	- Performance Eval: MLFlow Experiment Tracking, `mlflow.evaluate`

+ Llama Guard
	- Real-time
	- Classify and mitigate LLM prompts/responses
	- Components: Taxonomy of Risks (violence, hate, suicide, etc.)
	- Guideline: the action to be done after positive classification
	- Input Guard: before model
	- Output Guard: after model
	- Multiple Message Parsing: supported

## GenAI Evaluation Techniques

+ Eval Techniques for LLM System Components
	- Benchmarking
	- General Metrics
	- Performance Metrics

+ LLM Eval vs ML Eval
	- LLMs are more black box
	- LLMs have no clear metrics
	- LLMs are heavier

+ Base Eval Technique - Loss
	- Measures: next token prediction accuracy
	- Only understands grammar 

+ Base Eval Technique - Perplexity
	- Perplexity: how well a model predicts a sample
	- When Low: High Confidence & Accuracy
	- When High: Low Confidence & Accuracy
	- Does NOT consider relavance/accurate response

+ Base Eval Technique - Toxicity
	- Uses pre-trained hate-speach model
	- When Low: low harm

+ Task-specific Eval Metrics
	- Tasks like: summarization, translation, question answering
	- MLFlow Example: `mlflow.evalute(x,evaluators)` where evaluators can be regression, classification, etc.
	- Supervised ones (like BLEU, ROUGE) needs good _reference datasets_

+ Task-specific Eval Technique - BLEU (BiLingual Evaluation Understudy)
	- Compares translated output <> reference
	- Supervised
	- Uses n-gram similarity
	- Task: Translation

+ Task-specific Eval Technique - ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
	- Compares summarized output to references
	- Supervised
	- Uses n-gram similarity
	- Task: Summarization
	- N-gram Recall: (Total Matching N-grams) / (Total N-grams)
	- ROUGE-1: Words (tokens)
	- ROUGE-2: bigrams
	- ROUGE-L: Longest common subsequence
	- ROUGE-Lsum: Summary-level ROUGE-L, ignores punctuations

+ Benchmarking
	- Compare Model against standard eval datasets
	- Domain-specific Reference Datasets: better than generic ones
	- Your Custom Benchmark: Usually the best
	- Mosaic AI Gauntlet: 35 benchmarks, 6 categories

+ **Unsupervised Eval Technique - LLM-as-Judge**
	- Needs: definition of good/bad
	- Needs: component-based rubric/eval-scale
	- Needs: 2-5 example input/outputs
	- No understanding
	- Bias/ethical concerns
	- Hallucination
	- Best Practice: Small Rubric Scales

+ Human-in-the-Loop
	- Improves accuracy
	- Handles ambiguities
	- Not scalable

+ MLFlow LLM Eval
	- Batch Comparisons: Compare Foundational Models with fine-tuned models 
	- Rapid/Scalable Experimentation: eval unstructured outputs rapidly
	- Cost-Effective: save time on human-eval
	- Supports LLM-as-Judge: `evaluate` module, supports custom metrics 
	- `mlflow.evaluate(callable, eval_data, targets="col", model_type="text-summarization")`