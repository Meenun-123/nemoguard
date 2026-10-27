import unittest
from ai.agent import NemoGuardAgent
from ai.model_client import MockModelClient

class TestWorkflow(unittest.TestCase):
    def test_agent_sync_execution(self):
        agent = NemoGuardAgent(model_client=MockModelClient())
        events = []
        
        summary = agent.run(
            task_id="test_sync",
            code="def vulnerable(x):\n    cursor.execute(f'SELECT * FROM u WHERE id={x}')\n",
            task_description="Remediate SQL injection",
            auto_verify=True,
            max_iterations=4,
            event_callback=lambda evt: events.append(evt)
        )

        self.assertEqual(summary["status"], "COMPLETED")
        self.assertGreaterEqual(summary["total_steps"], 1)
        self.assertGreaterEqual(len(events), 2)
        self.assertTrue(any(e.event_type == "COMPLETED" for e in events))
        self.assertIn("patch", summary)
        self.assertTrue(summary["patch"]["valid_diff"])

    def test_fastapi_endpoints_if_available(self):
        try:
            from fastapi.testclient import TestClient
            from services.api.main import app
            client = TestClient(app)
            res = client.get("/api/v1/health")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()["status"], "healthy")
        except ImportError:
            # FastAPI or TestClient not installed yet in this environment; skip
            pass

if __name__ == "__main__":
    unittest.main()
