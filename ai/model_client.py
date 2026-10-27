import os
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import requests
from shared.config import settings

class BaseModelClient(ABC):
    """Abstract interface for NemoGuard model clients."""

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """Generate a completion response from the model."""
        pass


class NebiusModelClient(BaseModelClient):
    """
    Client for NVIDIA models served on Nebius Token Factory.
    Uses standard HTTP REST API with exponential backoff and timeout handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_id: Optional[str] = None
    ):
        self.api_key = api_key or settings.nebius_api_key
        self.base_url = (base_url or settings.nebius_base_url).rstrip("/")
        self.model_id = model_id or settings.nvidia_model_id

        if not self.api_key or self.api_key == "mock-key":
            raise ValueError(
                "NebiusModelClient requires a valid NEBIUS_API_KEY. "
                "Set NEBIUS_API_KEY in .env or switch AI_EXECUTION_MODE to 'mock'."
            )

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        start_time = time.time()
        max_retries = 3
        backoff = 1.5
        endpoint = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=settings.tool_execution_timeout_seconds
                )
                
                if response.status_code == 401:
                    raise PermissionError("Nebius Token Factory authentication failed. Check NEBIUS_API_KEY.")
                elif response.status_code == 429:
                    time.sleep(backoff ** (attempt + 1))
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                latency = round(time.time() - start_time, 3)
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})

                return {
                    "content": content,
                    "model": self.model_id,
                    "latency_seconds": latency,
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0)
                    },
                    "mode": "remote_nebius"
                }

            except (requests.exceptions.RequestException, PermissionError) as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Nebius Token Factory request failed after {max_retries} attempts: {str(e)}"
                    )
                time.sleep(backoff ** attempt)


class MockModelClient(BaseModelClient):
    """
    Deterministic mock client for offline development and CPU testing.
    Emulates NVIDIA Llama-3.1-Nemotron-70B multi-step reasoning outputs.
    """

    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id or settings.nvidia_model_id

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        start_time = time.time()
        last_message = messages[-1]["content"] if messages else ""

        # Determine step in ReAct reasoning chain
        if "reproduction_test" in last_message.lower():
            mock_content = json.dumps({
                "action": "run_sandbox_test",
                "action_input": {
                    "test_code": "def test_exploit():\n    assert process_user({'id': '1 OR 1=1'}) != 'ALL_DATA'"
                },
                "thought": "Synthesizing an automated reproduction test to confirm vulnerability."
            })
        elif "tool_result" in last_message.lower():
            mock_content = json.dumps({
                "action": "generate_patch",
                "action_input": {
                    "file_path": "target.py",
                    "explanation": "Replaced string concatenation SQL query with parameterized query execution to prevent SQL injection.",
                    "diff": "--- target.py\n+++ target.py\n@@ -2,3 +2,3 @@\n-    query = f'SELECT * FROM users WHERE id = {data[\"id\"]}'\n-    return db.execute(query)\n+    query = 'SELECT * FROM users WHERE id = ?'\n+    return db.execute(query, (data['id'],))"
                },
                "thought": "Security scanner identified SQL injection vulnerability. Synthesizing parameterized patch."
            })
        else:
            mock_content = json.dumps({
                "action": "run_security_scanner",
                "action_input": {"rule_set": "owasp_top_10"},
                "thought": "Analyzing source AST for security vulnerabilities, injection risks, and sanitization flaws."
            })

        latency = round(time.time() - start_time + 0.05, 3)
        return {
            "content": mock_content,
            "model": f"{self.model_id} (Deterministic Mock)",
            "latency_seconds": latency,
            "usage": {
                "prompt_tokens": 128,
                "completion_tokens": 94,
                "total_tokens": 222
            },
            "mode": "mock_local"
        }


def get_model_client() -> BaseModelClient:
    """Factory function returning the configured model client."""
    if settings.ai_execution_mode.lower() == "remote":
        return NebiusModelClient()
    return MockModelClient()
