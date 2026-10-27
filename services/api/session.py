import asyncio
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from services.api.schemas import AgentEvent, AnalyzeRequest
from ai.agent import NemoGuardAgent

class SessionManager:
    """Manages asynchronous tasks, agent executions, and live event streaming."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.event_queues: Dict[str, asyncio.Queue] = {}

    def create_task(self, req: AnalyzeRequest) -> str:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.tasks[task_id] = {
            "task_id": task_id,
            "status": "QUEUED",
            "request": req.dict(),
            "created_at": datetime.utcnow().isoformat(),
            "result": None
        }
        self.event_queues[task_id] = asyncio.Queue()
        return task_id

    async def run_agent_task(self, task_id: str):
        task_data = self.tasks.get(task_id)
        if not task_data:
            return

        task_data["status"] = "RUNNING"
        req = AnalyzeRequest(**task_data["request"])
        queue = self.event_queues.get(task_id)

        loop = asyncio.get_event_loop()

        def on_event(event: AgentEvent):
            if queue:
                # Thread-safe queue delivery
                asyncio.run_coroutine_threadsafe(queue.put(event), loop)

        agent = NemoGuardAgent()

        try:
            # Run the agent in executor thread so it doesn't block async event loop
            summary = await loop.run_in_executor(
                None,
                agent.run,
                task_id,
                req.code,
                req.task_description,
                req.auto_verify,
                req.max_iterations,
                on_event
            )
            task_data["status"] = "COMPLETED"
            task_data["result"] = summary
        except Exception as e:
            task_data["status"] = "FAILED"
            task_data["error"] = str(e)
            if queue:
                err_event = AgentEvent(
                    task_id=task_id,
                    step=99,
                    event_type="ERROR",
                    message=f"Agent failed: {str(e)}"
                )
                await queue.put(err_event)
        finally:
            if queue:
                # End of stream sentinel
                await queue.put(None)

    async def get_events(self, task_id: str):
        queue = self.event_queues.get(task_id)
        if not queue:
            return

        while True:
            event = await queue.get()
            if event is None:
                break
            yield event

session_manager = SessionManager()
