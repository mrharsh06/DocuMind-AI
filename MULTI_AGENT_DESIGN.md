#DocuMind AI -Multi-Agent System Design

##Overview

DocuMind AI is currently uses a single-service RAG(Retrieval Augmented Generation) approach where "QueryService" handles everything relevant chunks,analyzing them,and generating answert in one step

A multi-agent system breaks this monolithic approach into specialized agents,each with a focused responsibility.Instead of one service doing everything ,we will have:

->Research Agent:Finds and retrieve relevant document chunks
->Analyzer Agent:Analyzes retrieved chunks for insights and patterns
->Fact Checker Agent: Verifies accuracy and consistency across sources
->Synthesizer Agent: Combines all information into a coherent final answer
->Orchestrator Agent: Coordinates the workflow and manages agent communication


## Current System (Single Service)

### How QueryService Works Now

Currently, `QueryService` in `app/services/query_service.py` handles the entire RAG pipeline in one class:

1. **Embedding Generation**: Creates embeddings for the user's question
2. **Vector Search**: Queries ChromaDB to find similar document chunks
3. **Context Assembly**: Combines retrieved chunks into a single context string
4. **Answer Generation**: Sends everything to Gemini LLM to generate the final answer

**Limitations:**
- All logic in one place (hard to test individual steps)
- No specialized analysis of retrieved chunks
- No fact-checking or verification step
- Difficult to explain which part of the process contributed to the answer
- Hard to add new capabilities (e.g., cross-referencing, contradiction detection)



## Proposed Multi-Agent Architecture### High-Level DesignThe multi-agent system will replace the monolithic `QueryService` with a coordinated team of specialized agents:


### Key Principles1. **Separation of Concerns**: Each agent has ONE clear responsibility 
2. **Sequential Workflow**: Agents work in a logical order (research → analyze → verify → synthesize) 
3. **Orchestrator Control**: One agent manages the entire workflow 
4. **Reusability**: Each agent can be used independently or in different workflows 
5. **Explainability**: We can trace which agent contributed what to the final answer


## Agent Roles### 1. Researcher Agent**Role:** Retrieves relevant document chunks from the vector store based on the user's question.
**Why We Need This Agent:**- Separates retrieval logic from answer generation
- Can be optimized independently (e.g., hybrid search, reranking)
- Makes it easy to test retrieval quality separately
- **Input:**- User's question (string)
- Number of chunks to retrieve (optional, default: 5)
**Output:**- List of relevant document chunks with metadata (file_name, chunk_index, similarity_score)

**What It Does:**
1. Generates embedding for the question (or uses ChromaDB default)
2. Queries ChromaDB vector store for similar chunks
3. Returns top N most relevant chunks with their metadata

**Location:** `app/core/agents/researcher.py`

### 2. Analyzer Agent
**Role:** Analyzes retrieved document chunks to extract key insights, patterns, and important information.

**Why We Need This Agent:**
- Current system just passes chunks directly to LLM - no analysis step
- Can identify important entities, dates, numbers, relationships
- Helps filter out irrelevant information before synthesis
- Interview-ready: Shows you understand the value of intermediate processing

**Input:**
- List of document chunks (from Researcher Agent)
- User's original question

**Output:**
- Key insights extracted from chunks
- Important facts, dates, numbers, entities
- Summary of what each chunk contributes

**What It Does:**
1. Receives chunks from Researcher Agent
2. Uses LLM to analyze each chunk for key information
3. Extracts important facts, patterns, and insights
4. Returns structured analysis

**Location:** `app/core/agents/analyzer.py`
### 3. Fact Checker Agent
**Role:** Verifies accuracy and consistency across multiple document chunks, flags contradictions.

**Why We Need This Agent:**
- Current system doesn't check if chunks contradict each other
- Can identify when different sources say different things
- Improves answer reliability
- Interview-ready: Shows you think about quality and reliability

**Input:**
- Analyzed insights (from Analyzer Agent)
- Original document chunks (from Researcher Agent)

**Output:**
- Verified facts (marked as consistent)
- Contradictions (if any chunks conflict)
- Confidence scores for each fact

**What It Does:**
1. Compares information across multiple chunks
2. Identifies contradictions or inconsistencies
3. Marks which facts are verified by multiple sources
4. Flags any conflicting information

**Location:** `app/core/agents/fact_checker.py`

### 4. Synthesizer Agent
**Role:** Combines all information (chunks, insights, verified facts) into a coherent, well-structured final answer.

**Why We Need This Agent:**
- Separates answer generation from retrieval/analysis
- Can use all the processed information (not just raw chunks)
- Produces better-structured answers
- Interview-ready: Shows you understand the synthesis step in RAG

**Input:**
- Original question
- Document chunks (from Researcher)
- Analyzed insights (from Analyzer)
- Verified facts (from Fact Checker)

**Output:**
- Final answer (well-structured, coherent)
- Source citations (which chunks were used)

**What It Does:**
1. Receives all processed information from other agents
2. Uses LLM to generate a coherent answer
3. Ensures answer addresses the question
4. Includes proper source citations

**Location:** `app/core/agents/synthesizer.py`

### 5. Orchestrator Agent
**Role:** Coordinates the entire workflow, manages communication between agents, handles errors.

**Why We Need This Agent:**
- Current system has no coordination layer
- Manages the sequence of agent execution
- Handles errors gracefully (if one agent fails)
- Interview-ready: Shows you understand orchestration patterns

**Input:**
- User's question
- Optional parameters (n_results, etc.)

**Output:**
- Final response (answer + sources)
- Workflow status (which agents ran successfully)

**What It Does:**
1. Receives user question
2. Calls Researcher Agent → gets chunks
3. Calls Analyzer Agent → gets insights
4. Calls Fact Checker Agent → gets verified facts
5. Calls Synthesizer Agent → gets final answer
6. Returns complete response to user

**Location:** `app/core/agents/orchestrator.py`

## Agent Workflow

### Step-by-Step Execution Flow

Here's exactly how the agents work together when a user asks a question:

1.User sends question: "What is the main topic of the document?"
2.Orchestrator Agent receives the question
├─ Logs the request
└─ Initializes workflow
3.Orchestrator → Researcher Agent
├─ Input: Question + n_results=5
├─ Researcher queries vector store
└─ Output: 5 relevant chunks with metadata
4.Orchestrator → Analyzer Agent
├─ Input: Chunks from Researcher + Original question
├─ Analyzer extracts insights from each chunk
└─ Output: Key insights, facts, patterns
5.Orchestrator → Fact Checker Agent
├─ Input: Chunks + Insights from Analyzer
├─ Fact Checker compares information across chunks
└─ Output: Verified facts, contradictions (if any)
6.Orchestrator → Synthesizer Agent
├─ Input: Question + Chunks + Insights + Verified facts
├─ Synthesizer generates final answer
└─ Output: Coherent answer with source citations
7.Orchestrator returns final response to user
└─ Response: { answer, sources, workflow_status }

### Error Handling

- If Researcher fails → Return error: "Could not retrieve documents"
- If Analyzer fails → Continue with raw chunks (graceful degradation)
- If Fact Checker fails → Continue without verification (warn in response)
- If Synthesizer fails → Return raw chunks as answer (fallback)

### Parallel vs Sequential Execution

**Current Design: Sequential** (agents run one after another)
- Simpler to implement and debug
- Each agent needs output from previous agent
- Easier to trace workflow

**Future Enhancement: Parallel** (some agents can run simultaneously)
- Researcher and Analyzer could potentially run in parallel
- Requires more complex orchestration
- Better performance but harder to debug



## Benefits of This Design

### 1. Better Answer Quality
- **Specialized Processing**: Each agent focuses on one task, doing it better
- **Fact Verification**: Fact Checker ensures consistency across sources
- **Structured Analysis**: Analyzer extracts insights before synthesis
- **Result**: More accurate, reliable answers

### 2. Interview-Ready Architecture
- **System Design Skills**: Shows you understand multi-agent systems
- **Separation of Concerns**: Demonstrates clean architecture principles
- **Explainability**: You can explain which agent did what
- **Result**: Strong talking points for interviews

### 3. Maintainability & Scalability
- **Easy to Test**: Each agent can be tested independently
- **Easy to Modify**: Change one agent without affecting others
- **Easy to Extend**: Add new agents (e.g., Summarizer, Translator) easily
- **Result**: Code that's easier to maintain and grow

### 4. Debugging & Monitoring
- **Traceable Workflow**: Can see exactly where issues occur
- **Agent-Level Logging**: Each agent logs its own operations
- **Error Isolation**: If one agent fails, others can still work
- **Result**: Easier to debug and monitor production systems

### 5. Production-Ready Features
- **Graceful Degradation**: System works even if some agents fail
- **Error Handling**: Proper error handling at each step
- **Performance**: Can optimize individual agents independently
- **Result**: More robust, production-ready system

### Comparison: Single Service vs Multi-Agent

| Aspect | Single Service (Current) | Multi-Agent (Proposed) |
|--------|-------------------------|------------------------|
| **Answer Quality** | Good | Better (with verification) |
| **Testability** | Hard (all logic together) | Easy (test each agent) |
| **Explainability** | Low | High (know which agent did what) |
| **Maintainability** | Medium | High (isolated changes) |
| **Interview Value** | Medium | High (shows advanced skills) |
| **Complexity** | Low | Medium (but worth it) |