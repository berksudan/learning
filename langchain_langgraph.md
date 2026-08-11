## LangChain
+ Model Parameters:
    - temperature (0=deterministic, 1=random)
    - max tokens (caps the output token size)
    - timeout (max time to cancel before the response)
    - max retries (max amount of times to retry a failed request)
+ LangChain is model agnostic
+ Streaming mode reduces the **perceived** latency
+ Checkpointer: by default snapshots the state at the end of each run then groups
+ agents with common Thread IDs share memory!
+ Agent State: by default only list_of_messages. Custom fields can be added.
+ MCP (Model Context Protocol): An open protocol that standardizes how your LLM applications connect to and work with your tools and data sources
+ MCP Servers are tools+resources+prompts
+ Tool Calls: Agent ITSELF adjusts its own state or retrieves runtime context
    - Accessing Information: `ToolRuntime`
+ Agent Context: agent <!-> context. agent <-> tool runtime <-> context  
+ Agent Context is immutable, agent state is mutable!
+ Read/write CustomState AND read context: uses tool+ToolRuntime
+ Multi-agent system: Multiple specialized agents for complex applications
+ Multi-agent system: supervisor (orchestration) +  subagents
+ Multi-agent system: Supervisor agent -> tools that invoke subagents
+ Middlewares in Agents:
    - f(x) within the loop
    - Examples: classifiers, human-in-the-loop
+ SummarizationMiddleware Params: mini-model, trigger (when this summarization will happen), keep (#messages to keep after deleting), custom summarization prompt
+ Node-Style Middleware (CustomMiddleware): Adjust an agent's state while running
    - Accessing Information: `State` + `Runtime`
    - Example: Trim all `ToolMessage`s.
    - `@before_agent`,`@after_agent` are called once before/after the agent 
    - `@before_model`,`@after_model` are called multiple times before/after model call 
+ HumanInTheLoopMiddleware:
    - Arguments: `interrupt_on={"read_email":False,"send_email":True, "my_sexy_tool":False}` -> False=Auto-Approve
    - Approve on Interrupt: `agent.invoke(Command(resume={"decisions":["type":"approve"]}))`
    - Reject on Interrupt: `agent.invoke(Command(resume={"decisions":["type":"reject", "message": "THE REASON FOR REJECTION"]}))`
    - Edit on Interrupt: `agent.invoke(Command(resume={"decisions":["type":"edit", "edited_action": {"name":"tool_name","args":{"body":""}}]}))`
+ Wrap-Style Middleware (CustomMiddleware): Adjusts an agents tools, prompt, model while running
    - Accessing Information: `ModelRequest`
    - Examples: swap model, give additional tools based on user role/permissions (from context), change language based on conversation
    - Dynamic Prompt Decorator: `@dynamic_prompt`, `def func(request:ModelRequest)`
    - Dynamic Tool Decorator: `@wrap_model_call`, `def func(request:ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse`
    - Helper Util here: `ModelRequest.override(tools=new_tools,model=new_model)`f
---



## RAG (Retrieval-Augmented Generation)

+ 3 Components: Ingestion, Retrieval, Synthesis
    - Ingestion: Docs -> Chunks -> Embeddings -> Index
    - Retrieval: Query -> Index -> Top K chunks
    - Synthesis: LLM -> Response
+ RAG Triad (in Retrieval): Query -> Context -> Response
+ RAG (and LLM) Evaluation:
    - Groundedness (how much based on the context) 
    - Cost (#tokens used x price/token)
    - Latency (in each token generation and total completion time)
    - Quality (Answer Relevance, Context Relevance)
        - Golden Set for Benchmarking
+ LLM Evals (Tradeoff: Scalable vs. Meaningful):
    - Traditional NLP Evals (most scalable) <-> BLEU/ROUGE score
    - MLM Evals
    - LLM Evals
    - Human Evals (most meaningful) <-> Human Users
    - Ground Truth Evals <-> Human Experts

+ Sentence Window Query Engine: fetches the sentence + its window
+ Auto Merge Chunk Tree Strategy: IF Most Child chunk nodes THEN use parent node
---


---

## LangGraph

There are a few standard parameters that we can set with chat models. Two of the most common are:

    model: the name of the model
    temperature: the sampling temperature

Temperature controls the randomness or creativity of the model's output where low temperature (close to 0) is more deterministic and focused outputs. This is good for tasks requiring accuracy or factual responses. High temperature (close to 1) is good for creative tasks or generating varied respons

----

Chat models in LangChain have a number of default methods. For the most part, we'll be using:

    stream: stream back chunks of the response
    invoke: call the chain on an input


----

```python

from langchain_openai import ChatOpenAI
gpt4o_chat = ChatOpenAI(model="gpt-4o", temperature=0)
gpt35_chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


from langchain_core.messages import HumanMessage

# Create a message
msg = HumanMessage(content="Hello world", name="Person who calls it")

# Message list
messages = [msg]

# Invoke the model with a list of messages 
gpt4o_chat.invoke(messages) ### Invoke is a default chat-model method
```

----

+ Agent ~= Control flow defined by an LLM
+ LangGraph = Balance reliability with control. Less control but more reliable!
+ LangGraph expresses custom control flows as graphs
+ LangGraph: Persistence, streaming, human-in-the-loop, controllability
+ Edge Types: Simple Edge (1-way), Conditional Edge (n-way)
+ Nodes = Python Functions
+ in_state -> node function -> out_state