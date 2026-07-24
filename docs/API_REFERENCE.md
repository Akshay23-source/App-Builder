# ForgeAI Gateway API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication Endpoints

### `POST /users/verify-firebase`
Exchanges a verified Firebase ID token for a ForgeAI JWT access token.
- **Headers**: `Authorization: Bearer <firebase_id_token>`
- **Response**:
  ```json
  {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "user": {
      "id": "uuid-v4",
      "firebase_uid": "...",
      "email": "user@example.com"
    }
  }
  ```

## Project Endpoints

### `POST /projects`
Creates a project and triggers the Planner Agent Celery workflow.
- **Headers**: `Authorization: Bearer <jwt_access_token>`
- **Body**:
  ```json
  {
    "name": "My SaaS App",
    "prompt": "A landing page for an AI video editor with pricing tables"
  }
  ```

### `GET /projects`
Lists all generated projects for the authenticated user.

### `GET /projects/{project_id}`
Returns complete project detail including Task DAG node statuses, agent logs, and emitted files.

### `GET /projects/{project_id}/preview`
Renders live preview of the generated project inside an HTML sandbox wrapper.

## WebSocket Streaming Endpoint

### `WS /ws/build/{project_id}`
Establishes a real-time bi-directional streaming socket to receive agent thoughts, status updates, DAG execution events, and emitted file payloads.
