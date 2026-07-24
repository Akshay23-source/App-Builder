# ForgeAI Engine & Frontend

## Overview
ForgeAI is a locally-run application builder featuring a Next.js frontend, a FastAPI gateway, and an in-process async worker DAG for task execution. It stores all local data in a SQLite database (`forgeai.db`).

## Architecture
- **Frontend**: Next.js Web App running on port `3000`.
- **Backend Gateway**: FastAPI Server running on port `8000`.
- **Task Orchestrator**: In-Process Async Worker DAG (e.g., `codegen_worker`, `docs_worker`, `debug_worker`).
- **Database**: SQLite.

## How to Run Locally

You can launch both the frontend and the backend simultaneously using the provided startup script:

```bash
python run_local.py
```
*(Or use `start_dev.bat` if you are on Windows)*

This script will start:
1. **Backend Gateway API**: accessible at `http://localhost:8000`
2. **Gateway API Docs (Swagger UI)**: accessible at `http://localhost:8000/docs`
3. **Frontend Web App**: accessible at `http://localhost:3000`

## Repository Structure
- `backend/`: FastAPI application, orchestrator logic, worker scripts (like code generation, debugging, docs), and API routing.
- `frontend/`: Next.js user interface application.
- `docs/`: Project documentation.
- `infra/`: Infrastructure and local setup scripts.
- `forgeai.db`: Local SQLite database.

## Testing
To run the automated end-to-end tests locally:
```bash
python test_e2e_local.py
```