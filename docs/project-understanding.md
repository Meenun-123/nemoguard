# Project Understanding & Hackathon Assessment

**Hackathon**: Nebius × NVIDIA Global AI Hackathon  
**Deadline**: October 30, 2026, at 10:00 a.m. Pacific Time  
**Repository**: Monorepo (`apps/web`, `services/api`, `ai/`, `shared/`, `tests/`, `docs/`)  
**Target Tracks**: Coding & Agentic Engineering / Best Apps and Agents  

---

## 1. Workspace State & Discovery Audit

### Verified Facts
1. **Initial Workspace**: The workspace directory (`c:\Users\pmeen\OneDrive\Desktop\nvdia_project`) was completely empty prior to initialization. No legacy code, manifests, or pre-existing repositories were present.
2. **Git Environment**: Git version 2.55 is installed locally. Git repository has been initialized on branch `main` with user `P Meenun Reddy` (`pmeenunreddy@gmail.com`).
3. **Runtime Environment**: Python 3.12.10 is available. Node.js/npm is not currently in the global system PATH.
4. **Hardware Profiles**:
   - **Developer A (User)**: NVIDIA GeForce RTX 4050 (8 GB VRAM), 16 GB System RAM.
   - **Developer B (Teammate)**: NVIDIA GeForce RTX 5050 (8 GB VRAM), 24 GB System RAM.
5. **Infrastructure**:
   - Nebius Token Factory provides an OpenAI-compatible REST API (`https://api.tokenfactory.nebius.com/v1/`) with Bearer token authentication via `NEBIUS_API_KEY`.
   - NVIDIA qualifying open-source models (notably `nvidia/Llama-3.1-Nemotron-70B-Instruct-HF` and Nemotron variants) are hosted on Nebius Token Factory.

### Assumptions & Open Confirmations
1. **Model Endpoint Availability**: Assumed that the project uses `nvidia/Llama-3.1-Nemotron-70B-Instruct-HF` via Nebius Token Factory for remote inference. Mock client mode is provided for offline development and local test automation so missing API keys never block development.
2. **Submission URL & Devpost**: Submissions are submitted via the official Devpost page with a public Git repository, open-source license (Apache 2.0), setup guide, and a <= 3 minute YouTube video demonstration.

---

## 2. Hardware Constraints & Mitigation

Both laptops have 8 GB VRAM GPUs (RTX 4050 and RTX 5050). 
- **Rule 1**: Never attempt to load 70B models locally. All heavyweight inference is offloaded to **Nebius Token Factory** via cloud API calls.
- **Rule 2**: Never assume GPUs can be pooled or that both laptops are online simultaneously.
- **Rule 3**: Local unit and integration tests must run fully offline on CPU using deterministic mocks (`AI_EXECUTION_MODE=mock`).
- **Rule 4**: Lightweight local models (e.g. small embedding or tokenization tasks) must strictly respect the 8 GB limit and be purely optional.

---

## 3. Project Selection: NemoGuard

### Project Name: **NemoGuard**
**Tagline**: Autonomous Agentic Code Vulnerability Detection, Reproduction & Self-Healing Engine powered by NVIDIA Nemotron on Nebius Token Factory.

### Problem Statement
Software teams lose hundreds of hours triaging complex vulnerabilities, race conditions, memory leaks, and logic regressions. Existing linters only flag issues with generic warnings, while standard chatbots hallucinate fixes that break adjacent code because they cannot run tests or inspect execution traces.

### The NemoGuard Solution
NemoGuard is an end-to-end agentic engineering platform that:
1. Takes a code snippet, module, or test failure report.
2. Uses **NVIDIA Nemotron 70B** on **Nebius Token Factory** with a multi-step reasoning loop (Observe -> Plan -> Tool Execution -> Verification).
3. Employs dedicated sandboxed analysis tools:
   - AST & security rule analyzer (detecting OWASP Top 10, concurrency bugs, unhandled exceptions).
   - Automated reproduction test synthesizer.
   - Patch generator producing unified diffs.
   - Verification runner evaluating syntax, regression safety, and test assertions.
4. Provides an interactive, real-time dashboard showing the agent's thought chain, tool invocations, live unified diff viewer, verification proof, and Nebius Token Factory inference telemetry.

### Why NemoGuard Wins
- **Real Agentic Engineering**: Not a simple chat prompt. It executes a structured state machine with bounded iterations, tool calls, and automated verification.
- **NVIDIA Model Showcase**: Highlights NVIDIA Nemotron-70B's superior reasoning, code understanding, and structured schema generation.
- **Nebius Cloud Native**: Built to consume Nebius Token Factory with real-time token tracking, latency instrumentation, and graceful degraded modes.
- **Demonstrable in 3 Minutes**: Clear before-and-after demonstration: feed an insecure/broken function -> watch agent plan and test -> see verified patch with passing tests.
