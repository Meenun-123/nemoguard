import os
from pathlib import Path

# Base repository directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Read .env manually if exists
env_path = ROOT_DIR / ".env"
if env_path.exists():
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("\"'")
                    if k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

class Settings:
    """Application settings with environment variable precedence."""

    def __init__(self):
        self.nebius_api_key = os.environ.get("NEBIUS_API_KEY", "mock-key")
        self.nebius_base_url = os.environ.get(
            "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"
        )
        self.nvidia_model_id = os.environ.get(
            "NVIDIA_MODEL_ID", "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"
        )
        self.ai_execution_mode = os.environ.get("AI_EXECUTION_MODE", "mock")
        self.api_host = os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = int(os.environ.get("API_PORT", 8000))
        self.environment = os.environ.get("ENVIRONMENT", "development")
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")
        self.max_agent_iterations = int(os.environ.get("MAX_AGENT_ITERATIONS", 5))
        self.tool_execution_timeout_seconds = int(
            os.environ.get("TOOL_EXECUTION_TIMEOUT_SECONDS", 30)
        )
        self.allow_destructive_actions = (
            os.environ.get("ALLOW_DESTRUCTIVE_ACTIONS", "false").lower() == "true"
        )

settings = Settings()
