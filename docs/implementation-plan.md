# NemoGuard: Implementation & Delivery Plan

## Phase Overview

| Phase | Milestone | Owner | Status |
|---|---|---|---|
| **Phase 1** | Workspace Inspection & Architecture Docs | Lead Engineer | Completed |
| **Phase 2** | Git Repository Initialization & Branch Strategy | Lead Engineer | In Progress |
| **Phase 3** | Shared Core & Model Client (`ai/model_client.py`) with Nebius & Mock | Developer B | Scheduled |
| **Phase 4** | Agent Loop & Tool Suite (`ai/agent.py`, `ai/tools/`) | Developer B | Scheduled |
| **Phase 5** | FastAPI Backend & SSE Streaming (`services/api/`) | Developer A | Scheduled |
| **Phase 6** | Interactive Web Dashboard (`apps/web/`) | Developer A | Scheduled |
| **Phase 7** | Unit & Integration Test Suite (`tests/`) | Both | Scheduled |
| **Phase 8** | README, Video Demo Script & Submission Prep | Both | Scheduled |

---

## Detailed Task Breakdown

### Milestone 1: Shared Core & Environment Configuration
- [x] Initialize Git repository with `main` branch.
- [x] Configure `.gitignore`, `LICENSE`, `.env.example`.
- [x] Establish architecture contracts and schemas.
- [ ] Create `shared/config.py` loading environment variables with fallback defaults.

### Milestone 2: Model Client (`ai/model_client.py`)
- [ ] Implement `NebiusModelClient` using standard OpenAI-compatible client interface.
- [ ] Implement `MockModelClient` generating realistic structured responses for local development.
- [ ] Add exponential backoff, retry logic, timeout handling, and token telemetry tracking.
- [ ] Implement unit tests in `tests/unit/test_model_client.py`.

### Milestone 3: AI Tools & Agent Orchestrator (`ai/`)
- [ ] Implement `security_scanner.py`: AST-based pattern scanner for Python code (SQL injection, unsafe eval, path traversal, hardcoded secrets).
- [ ] Implement `test_runner.py`: Executes synthesized pytest/unittest assertions safely.
- [ ] Implement `patch_validator.py`: Validates diff syntax and code compilability.
- [ ] Implement `NemoGuardAgent`: Multi-step reasoning loop (Observe -> Plan -> Execute Tool -> Evaluate -> Conclude).

### Milestone 4: Backend API & Streaming (`services/api/`)
- [ ] Implement FastAPI application with CORS and static file mounting.
- [ ] Implement health check (`/api/v1/health`).
- [ ] Implement analysis submission (`POST /api/v1/analyze`).
- [ ] Implement Server-Sent Events stream (`GET /api/v1/stream/{task_id}`).
- [ ] Implement mock test coverage for API endpoints.

### Milestone 5: Web UI Dashboard (`apps/web/`)
- [ ] Build responsive, clean single-page dashboard with zero heavy external build dependencies.
- [ ] Code input editor with sample vulnerability presets (SQL injection, unsafe deserialization, race condition).
- [ ] Live streaming agent execution timeline (thought, tool calls, results).
- [ ] Side-by-side / inline unified diff viewer for proposed patch.
- [ ] Verification badge and Nebius telemetry card (model ID, latency, token count).

### Milestone 6: End-to-End Verification & Documentation
- [ ] Run full test suite (`python scripts/run_tests.py`).
- [ ] Validate end-to-end smoke test in both `mock` and `remote` modes.
- [ ] Complete comprehensive `README.md` with setup guide, architecture diagrams, and run commands.
- [ ] Prepare 3-minute video demo script and slides.
