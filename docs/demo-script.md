# NemoGuard: 3-Minute Hackathon Video Demonstration Script
**Competition**: Nebius × NVIDIA Global AI Hackathon  
**Target Duration**: 2 minutes 45 seconds (Under the 3:00 official limit)  
**Presenters**: Team NemoGuard (Developer A & Developer B)

---

## Storyboard & Timing Breakdown

### 0:00 – 0:30 | The Problem: Why Linters & Generic Chatbots Fail
- **Visual**: Screen recording showing a real-world insecure Python endpoint (SQL injection / CWE-89) in the NemoGuard dashboard.
- **Narrator (Developer A)**:
  > *"Every engineering team loses hours triaging security vulnerabilities. Traditional linters give static warnings without context, while generic chatbots hallucinate broken code because they cannot run tests or inspect execution traces. We built **NemoGuard** — an autonomous agentic engineering engine that doesn't just guess a fix; it proves the vulnerability, synthesizes a patch, and verifies it in a closed-loop sandbox."*

---

### 0:30 – 1:15 | The Core AI Engine: NVIDIA Nemotron 70B & Nebius Token Factory
- **Visual**: Switch to the **Nebius Telemetry** tab. Highlight the **Nebius vs. Local Benchmark Card** showing 55x speedup and 0% local VRAM pressure.
- **Narrator (Developer B)**:
  > *"At the heart of NemoGuard is **NVIDIA Llama-3.1-Nemotron-70B-Instruct**, running on **Nebius Token Factory**. A 70B reasoning model requires up to 70 GB of VRAM — completely impossible to run on standard 8 GB developer laptops. By leveraging Nebius Token Factory's high-throughput GPU API, we achieve 80+ tokens per second with sub-second decision latency and zero memory pressure on developer machines."*

---

### 1:15 – 2:10 | Live Demonstration: 4-Step Autonomous Engineering Cycle
- **Visual**: Click **"Launch NemoGuard Agent"**. Watch the live visual stepper advance through:
  1. **AST Security Scanner**: Flags SQL injection (CWE-89 / OWASP A03).
  2. **Reproduction Test**: Generates automated unit assertion confirming the exploit.
  3. **Patch Synthesis**: Synthesizes the parameterized query unified diff.
  4. **Sandbox Verification**: Runs in-memory assertions, proving 100% test pass.
- **Narrator (Developer A)**:
  > *"Watch our agent in action. As we click 'Launch Agent', Nemotron-70B begins a structured ReAct loop. Step 1: it uses our custom AST tool to identify string-concatenated SQL queries. Step 2: it autonomously synthesizes a reproduction test to prove the exploit. Step 3: it generates a unified diff replacing dynamic strings with safe parameterized placeholders. Step 4: our sandboxed runner executes the patch against reproduction assertions, verifying immunity without breaking adjacent logic."*

---

### 2:10 – 2:40 | Interactive Verification & Audit Report
- **Visual**: 
  - Toggle **Side-by-Side Split View** in the **Verified Patch Diff** tab.
  - Switch to **Verification Proof** tab and type `' OR '1'='1' --` into the **Interactive Exploit Playground** and click **"Test Immunity"**.
  - Click **"📄 Export Audit Report"** to download the Markdown audit artifact.
- **Narrator (Developer B / A)**:
  > *"Developers can inspect the diff side-by-side or test custom attack payloads directly in our interactive exploit playground to prove immunity. With one click, they can export a complete Markdown security audit report containing the full evidence trail, synthesized reproduction code, unified patch, and Nebius telemetry proof."*

---

### 2:40 – 2:55 | Conclusion & Compliance
- **Visual**: Show the public GitHub repository ([github.com/Meenun-123/nemoguard](https://github.com/Meenun-123/nemoguard)) with Apache 2.0 license, clean tests, and documentation.
- **Narrator**:
  > *"NemoGuard is open source under Apache 2.0, fully reproducible offline with deterministic mock testing, and ready for deployment on Nebius AI Cloud. Built for the Nebius × NVIDIA Global AI Hackathon. Thank you!"*
