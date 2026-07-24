# ForgeAI Agent Prompts & System Role Catalog

This document details the system prompts used by each specialized agent in the ForgeAI platform.

## 1. Planner Agent (`backend/agents/prompts/planner.md`)
- **Primary Provider**: Anthropic (Claude 3.5 Sonnet)
- **Role**: Breaks user prompt into a structured JSON execution DAG containing dependencies, tech stack requirements, and metadata.

## 2. Research Agent (`backend/agents/prompts/research.md`)
- **Primary Provider**: Google Gemini + Tavily Search
- **Role**: Performs live web search grounding for UI design tokens, typography, component hierarchies, and competitor patterns.

## 3. CodeGen Agent (`backend/agents/prompts/codegen.md`)
- **Primary Provider**: OpenAI GPT-4o (Fallback: DeepSeek Coder)
- **Role**: Generates complete Next.js 14 App Router project file tree as JSON `{"files": [{"path": "...", "content": "..."}]}`.

## 4. Debug Agent (`backend/agents/prompts/debug.md`)
- **Primary Provider**: OpenAI GPT-4o
- **Role**: Receives sandbox build error traces from `npm run build`, identifies broken symbols or imports, and emits repaired files.

## 5. Documentation Agent (`backend/agents/prompts/docs.md`)
- **Primary Provider**: Anthropic (Claude 3.5 Sonnet)
- **Role**: Produces README.md and component architecture documentation for the generated application.
