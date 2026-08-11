### Agentic AI & LLM Orchestration Patterns

- [ ] 1.5h — LangChain Academy: Intro to LangGraph (modules 1-4: state, nodes, edges, branching) https://academy.langchain.com/courses/intro-to-langgraph
- [ ] 1h — LangChain Academy: modules 5-7 (persistence, human-in-the-loop, memory) https://academy.langchain.com/courses/intro-to-langgraph
- [ ] 30min — LangGraph multi-agent conceptual guide (supervisor, swarm, handoffs) https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- [ ] 45min — Anthropic: Building Effective Agents (read fully, note orchestrator/subagent/tool-use patterns) https://www.anthropic.com/research/building-effective-agents
- [ ] 1h — DeepLearning.AI: AI Agents in LangGraph (short course, watch all) https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- [ ] 1h — DeepLearning.AI: Functions, Tools and Agents with LangChain https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
- [ ] 15min — LangGraph how-to: streaming in agents https://langchain-ai.github.io/langgraph/how-tos/streaming/
- [ ] 45min — Instructor library: concepts + quickstart (Pydantic-based structured LLM outputs) https://python.useinstructor.com/concepts/models/
- [ ] 45min — OpenAI structured outputs guide (schema validation, tool use, JSON mode) https://platform.openai.com/docs/guides/structured-outputs
- [ ] Microsoft multi-agent reference architecture https://microsoft.github.io/multi-agent-reference-architecture/index.html

---

### RAG, Evaluation & Azure Stack

- [ ] 1.5h — DeepLearning.AI: Building and Evaluating Advanced RAG (sentence-window, auto-merging, reranking) https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- [ ] 45min — Azure AI Search: hybrid search overview (BM25 + vector + semantic reranker) https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
- [ ] 45min — Azure AI Search: vector search concepts & index design https://learn.microsoft.com/en-us/azure/search/vector-search-overview
- [ ] 1h — DeepLearning.AI: Evaluating and Debugging Generative AI (golden sets, human review, monitoring) https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/
- [ ] 45min — RAGAS docs: faithfulness, answer relevancy, context recall (understand each metric) https://docs.ragas.io/en/latest/concepts/metrics/
- [ ] 45min — MLflow LLM Evaluate: how to log and compare LLM eval runs https://mlflow.org/docs/latest/llms/llm-evaluate/
- [ ] 30min — MLflow AI Gateway & prompt engineering UI overview https://mlflow.org/docs/latest/llms/deployments/
- [ ] 1h — Azure AI Foundry: overview, model catalog, deployments, prompt flow https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry
- [ ] 30min — Azure AI Foundry Agent Service (Azure-native agent runtime) https://learn.microsoft.com/en-us/azure/ai-services/agents/overview
- [ ] 30min — Azure AI Foundry: built-in evaluation (safety, groundedness, relevance) https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai

---

### Production Patterns & Interview Simulation

- [ ] 45min — FastAPI + async IO guide (async endpoints, background tasks, lifespan) https://fastapi.tiangolo.com/async/
- [ ] 30min — Python asyncio: gather, TaskGroup, timeouts (the patterns that matter for AI pipelines) https://docs.python.org/3/library/asyncio-task.html
- [ ] 1h — Eugene Yan: Patterns for LLM Systems (evals, RAG, agents, caching; read all sections) https://eugeneyan.com/writing/llm-patterns/
- [ ] 30min — Guardrails AI: validators, rail specs, output correction https://www.guardrailsai.com/docs/concepts/guard
- [ ] 30min — Azure Monitor + Application Insights for AI workloads (observability angle) https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
- [ ] 30min — Azure Key Vault + Managed Identity: the access pattern for enterprise AI systems https://learn.microsoft.com/en-us/azure/key-vault/general/developers-guide

**(2h) — Simulation & story prep**

No new material. Use this time to prep answers for the questions the interviewer will almost certainly ask:

- "Walk me through a multi-agent system you built"
  - Cover: graph topology, state design, failure modes, how you handled retries and fallbacks
- "How do you evaluate an LLM system before shipping?"
  - Cover: golden sets, offline benchmarks, human review, production monitoring; map to RAGAS metrics
- "How did you handle latency vs quality trade-offs in a RAG system?"
  - Cover: chunking strategy, reranker cost, async retrieval, caching
- "How do you integrate an AI system into an enterprise Azure environment?"
  - Cover: Managed Identity, Key Vault, private endpoints, App Insights
- "When would you NOT use an LLM?"
  - Cover: deterministic rules, latency constraints, cost, auditability requirements



### Books
- Book (O’Reilly): AI Engineering: Building Applications with Foundation Models — End-to-end product + system design on top of FMs; evaluation strategies to ship safer, better apps.
- Book (O’Reilly): Hands-On Large Language Models: Language Understanding and Generation — Code-first projects (summarization, semantic search, classification) + the practical LLM foundations.