import json
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from shared.config import settings, ROOT_DIR
from services.api.schemas import AnalyzeRequest, TaskResponse, HealthResponse
from services.api.session import session_manager

app = FastAPI(
    title="NemoGuard API",
    description="Autonomous Agentic Vulnerability Remediation powered by NVIDIA Nemotron on Nebius Token Factory",
    version="1.0.0"
)

# Enable CORS for local and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoints (Supports both /health and /api/v1/health)
@app.get("/health", response_model=HealthResponse)
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        execution_mode=settings.ai_execution_mode,
        model_id=settings.nvidia_model_id,
        nebius_base_url=settings.nebius_base_url,
        max_iterations=settings.max_agent_iterations
    )

# Submit Code for Agentic Remediation
@app.post("/api/v1/analyze", response_model=TaskResponse, status_code=202)
async def analyze_code(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    task_id = session_manager.create_task(req)
    background_tasks.add_task(session_manager.run_agent_task, task_id)
    task_info = session_manager.tasks[task_id]
    return TaskResponse(
        task_id=task_id,
        status=task_info["status"],
        created_at=task_info["created_at"]
    )

# Real-Time SSE Stream for Agent Thoughts and Actions
@app.get("/api/v1/stream/{task_id}")
async def stream_task_events(task_id: str):
    if task_id not in session_manager.tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    async def event_generator():
        async for event in session_manager.get_events(task_id):
            payload = json.dumps(event.dict())
            yield f"data: {payload}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# Task Status Query
@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = session_manager.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Static Web Dashboard Frontend Mount
web_dir = ROOT_DIR / "apps" / "web"
static_dir = web_dir / "static"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/")
async def serve_index():
    index_file = web_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "NemoGuard API is running. apps/web/index.html not found."}
