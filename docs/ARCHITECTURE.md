# ForgeAI System Architecture & Engineering Specifications

ForgeAI turns a single prompt idea into a complete, runnable Next.js 14 web application using a multi-agent task graph and isolated sandbox verification loop.

## Architecture Overview

```
Frontend (Next.js 14 App Router + Tailwind + Framer Motion)
   │  Google OAuth + Phone OTP (Firebase Auth)
   ▼
API Gateway (FastAPI)
   │  Token validation, rate-limiting, REST API & WebSocket Stream
   ▼
Orchestrator Service (FastAPI + Celery + Redis + Postgres)
   │  Evaluates Task DAG → dispatches agents → broadcasts Redis stream
   ▼
┌───────────┬───────────┬────────────┬───────────┬───────────────┐
│ Planner   │ Research  │ CodeGen    │ Debug     │ Documentation │
│ Agent     │ Agent     │ Agent      │ Agent     │ Agent         │
└───────────┴───────────┴────────────┴───────────┴───────────────┘
   │
   ▼
AI Provider Router (Adapter Pattern)
   ├── Anthropic (Claude 3.5 Sonnet) → Planner & Docs
   ├── OpenAI (GPT-4o) → CodeGen & Debug
   ├── DeepSeek (DeepSeek Coder) → Low-cost CodeGen fallback
   ├── Google Gemini (Gemini 1.5 Pro) → Research & Summarization
   └── Tavily Search API → Live Web Search Grounding
   │
   ▼
Sandboxed Build Executor (Node.js Sandbox)
   │ Writes files to /backend/sandbox/workspace/{project_id}/
   │ Runs `npm install && npm run build`
   └── Feeds error stack traces back to Debug Agent (Max 3 repair retries)
```

## Key Architectural Decisions

1. **Adapter Pattern for AI Providers (`backend/providers/`)**:
   Every agent invokes `provider_router.complete_for_role(role, prompt)`. Provider swap or fallback execution requires zero agent code changes.

2. **Task Execution DAG (`backend/orchestrator/task_graph.py`)**:
   Tasks are executed based on dependency graphs. Independent tasks (e.g. Research and initial file prep) run concurrently in parallel Celery workers.

3. **Strict JSON Protocol for CodeGen**:
   CodeGen Agent outputs a raw JSON file tree `{"files": [{"path": "...", "content": "..."}]}` ensuring buildable apps rather than plain prose code snippets.

4. **Automated Sandbox Build & Repair Loop**:
   Debug Agent compiles the emitted project inside a Node sandbox environment. If compilation fails, build logs are sent back for up to 3 repair iterations.
