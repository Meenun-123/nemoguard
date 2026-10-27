# Team Workflow & Git Collaboration Guide

## 1. Team Allocation

- **Developer A (User - Laptop 1, RTX 4050)**:
  - **Ownership**: Frontend Web UI (`apps/web/`), API endpoints & routing (`services/api/`), contracts & integration tests.
  - **Branch**: `feat/frontend`
- **Developer B (Teammate - Laptop 2, RTX 5050)**:
  - **Ownership**: AI Core (`ai/`), Nebius model client & integration, prompt templates, agent tools, AI unit tests.
  - **Branch**: `feat/ai-core`

---

## 2. Git Branch Strategy

```text
main (Protected, stable, always deployable)
  │
  ├── feat/frontend  (Developer A)
  └── feat/ai-core   (Developer B)
```

### Workflow Rules:
1. **Never commit directly to `main` without testing**: Both developers work on their feature branches (`feat/frontend`, `feat/ai-core`).
2. **Pull before starting new work**: Run `git checkout main && git pull origin main` before branching or rebasing.
3. **Small, descriptive commits**: Commit logical units with prefixes:
   - `feat:` new feature
   - `fix:` bug fix
   - `test:` test coverage
   - `docs:` documentation
4. **Merge integration**: When both feature branches pass local tests (`python scripts/run_tests.py`), merge them into `main`.
5. **No secret commits**: Never commit `.env` or API keys. `.env.example` contains placeholders only.

---

## 3. Remote Repository Setup (GitHub)

Follow these exact steps to connect this local repository to GitHub:

### Step 1: Create a Repository on GitHub
1. Open your browser and navigate to [github.com/new](https://github.com/new).
2. Repository name: `nemoguard` (or `nebius-nvidia-hackathon`).
3. Set visibility to **Public** (required by hackathon rules).
4. Do **not** initialize with a README, .gitignore, or license (we already created them locally).
5. Click **Create repository**.

### Step 2: Link Local Repository and Push
Run the following commands in this workspace terminal:

```bash
# Add the remote origin (replace YOUR-USERNAME and REPO-NAME with your GitHub details)
git remote add origin https://github.com/YOUR-USERNAME/nemoguard.git

# Push the initial main branch
git push -u origin main

# Create and push Developer A's branch
git checkout -b feat/frontend
git push -u origin feat/frontend

# Create and push Developer B's branch
git checkout -b feat/ai-core
git push -u origin feat/ai-core
```

---

## 4. Teammate (Developer B) Setup Instructions

Send these instructions to Developer B:

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/nemoguard.git
   cd nemoguard
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment configuration:
   ```bash
   cp .env.example .env
   # Update NEBIUS_API_KEY if testing live remote inference
   ```
5. Checkout your feature branch:
   ```bash
   git checkout feat/ai-core
   ```
6. Run the local test suite (runs on CPU/mock, zero GPU needed):
   ```bash
   python scripts/run_tests.py
   ```
