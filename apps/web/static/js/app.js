// NemoGuard Frontend Application Logic

const PRESETS = {
  sql_injection: `def get_user_profile(user_input):\n    # VULNERABLE: Direct string formatting in SQL statement\n    query = f"SELECT * FROM users WHERE username = '{user_input}' AND active = 1"\n    cursor.execute(query)\n    return cursor.fetchall()`,
  
  eval_rce: `def evaluate_math_expression(user_payload):\n    # VULNERABLE: Direct dynamic code execution\n    expr = user_payload.get("expression")\n    result = eval(expr)\n    return {"result": result}`,
  
  shell_injection: `import subprocess\n\ndef ping_host(host_ip):\n    # VULNERABLE: Shell command execution with shell=True\n    cmd = f"ping -c 1 {host_ip}"\n    output = subprocess.check_output(cmd, shell=True)\n    return output.decode()`,
  
  api_key: `import requests\n\ndef query_external_service():\n    # VULNERABLE: Hardcoded high-privilege API token\n    api_key = "SAMPLE_HARDCODED_SERVICE_TOKEN_KEY_ABC123"\n    headers = {"Authorization": f"Bearer {api_key}"}\n    return requests.get("https://api.example.com/data", headers=headers).json()`
};

document.addEventListener("DOMContentLoaded", () => {
  const codeInput = document.getElementById("code-input");
  const presetSelector = document.getElementById("preset-selector");
  const runBtn = document.getElementById("run-btn");
  const taskDesc = document.getElementById("task-desc");
  const autoVerify = document.getElementById("auto-verify");
  const modeBadge = document.getElementById("mode-badge");
  const timelineStream = document.getElementById("timeline-stream");
  const diffContainer = document.getElementById("diff-container");
  const verificationCard = document.getElementById("verification-card");
  const tabBtns = document.querySelectorAll(".tab-btn");

  // Load default preset
  codeInput.value = PRESETS.sql_injection;

  presetSelector.addEventListener("change", (e) => {
    codeInput.value = PRESETS[e.target.value] || "";
  });

  // Check health and backend execution mode
  fetch("/api/v1/health")
    .then(res => res.json())
    .then(data => {
      modeBadge.textContent = data.execution_mode.toUpperCase() === "REMOTE" 
        ? "MODE: REMOTE (Nebius AI)" 
        : "MODE: MOCK (Local 8GB Dev)";
      document.getElementById("tel-model").textContent = data.model_id;
    })
    .catch(() => {
      modeBadge.textContent = "MODE: OFFLINE";
    });

  // Tab switching
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(tc => tc.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });

  // Run Agent Workflow
  runBtn.addEventListener("click", async () => {
    const code = codeInput.value.trim();
    if (!code) {
      alert("Please provide code to analyze.");
      return;
    }

    runBtn.disabled = true;
    runBtn.innerHTML = `<span class="btn-icon">⏳</span> Reasoning in Progress...`;
    timelineStream.innerHTML = "";
    diffContainer.innerHTML = `<div class="empty-state"><p>Generating patch...</p></div>`;
    verificationCard.innerHTML = `<div class="empty-state"><p>Awaiting verification test...</p></div>`;

    try {
      const res = await fetch("/api/v1/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: code,
          task_description: taskDesc.value,
          auto_verify: autoVerify.checked,
          max_iterations: 5
        })
      });

      if (!res.ok) throw new Error("Failed to start analysis task");
      const { task_id } = await res.json();

      // Listen to SSE stream
      const eventSource = new EventSource(`/api/v1/stream/${task_id}`);

      eventSource.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        handleAgentEvent(payload);

        if (payload.event_type === "COMPLETED" || payload.event_type === "ERROR") {
          eventSource.close();
          runBtn.disabled = false;
          runBtn.innerHTML = `<span class="btn-icon">⚡</span> Run NemoGuard Agent`;
        }
      };

      eventSource.onerror = () => {
        eventSource.close();
        runBtn.disabled = false;
        runBtn.innerHTML = `<span class="btn-icon">⚡</span> Run NemoGuard Agent`;
      };

    } catch (err) {
      alert(`Error starting agent: ${err.message}`);
      runBtn.disabled = false;
      runBtn.innerHTML = `<span class="btn-icon">⚡</span> Run NemoGuard Agent`;
    }
  });

  function handleAgentEvent(evt) {
    const eventCard = document.createElement("div");
    eventCard.className = `timeline-event event-${evt.event_type}`;

    eventCard.innerHTML = `
      <div class="event-header">
        <span>STEP ${evt.step} • ${evt.event_type}</span>
        <span>${new Date(evt.timestamp).toLocaleTimeString()}</span>
      </div>
      <div class="event-body">${escapeHtml(evt.message)}</div>
    `;

    timelineStream.appendChild(eventCard);
    timelineStream.scrollTop = timelineStream.scrollHeight;

    // Handle Patch Generated
    if (evt.event_type === "PATCH_GENERATED" && evt.data) {
      renderDiff(evt.data.diff, evt.data.explanation);
    }

    // Handle Verification Result
    if (evt.event_type === "VERIFICATION_RESULT" && evt.data) {
      renderVerification(evt.data);
    }

    // Handle Completed Telemetry
    if (evt.event_type === "COMPLETED" && evt.data) {
      document.getElementById("tel-tokens").textContent = `${evt.data.total_tokens} tokens`;
      document.getElementById("tel-latency").textContent = `${evt.data.elapsed_seconds}s`;

      // Add completion checkmarks on tabs
      const patchTabBtn = document.querySelector('[data-tab="patch-tab"]');
      if (patchTabBtn && !patchTabBtn.innerHTML.includes("✓")) {
        patchTabBtn.innerHTML = `Verified Patch Diff <span style="color: #3fb950; font-weight: bold;">✓</span>`;
      }
      const verifTabBtn = document.querySelector('[data-tab="verification-tab"]');
      if (verifTabBtn && !verifTabBtn.innerHTML.includes("✓")) {
        verifTabBtn.innerHTML = `Verification Proof <span style="color: #3fb950; font-weight: bold;">✓</span>`;
      }
    }
  }

  function renderDiff(diffText, explanation) {
    if (!diffText) return;
    const lines = diffText.split("\n").map(line => {
      if (line.startsWith("+")) return `<div class="diff-add">${escapeHtml(line)}</div>`;
      if (line.startsWith("-")) return `<div class="diff-rem">${escapeHtml(line)}</div>`;
      return `<div>${escapeHtml(line)}</div>`;
    }).join("");

    diffContainer.innerHTML = `
      <div style="margin-bottom: 0.8rem; font-size: 0.9rem; color: #8b949e;">
        <strong>Remediation Strategy:</strong> ${escapeHtml(explanation || "")}
      </div>
      <pre><code>${lines}</code></pre>
    `;
  }

  function renderVerification(data) {
    const statusColor = data.passed ? "#238636" : "#da3633";
    const statusText = data.passed ? "VERIFICATION PASSED" : "VERIFICATION FAILED";

    verificationCard.innerHTML = `
      <div style="padding: 1rem; border-left: 4px solid ${statusColor}; background: #0b0e14; border-radius: 4px;">
        <h3 style="color: ${statusColor}; font-size: 1rem; margin-bottom: 0.5rem;">${statusText}</h3>
        <p style="font-size: 0.85rem; color: #8b949e;">Execution Duration: ${data.duration_seconds}s</p>
        ${data.error ? `<pre style="margin-top: 0.5rem; color: #f85149;">${escapeHtml(data.error)}</pre>` : ""}
      </div>
    `;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
