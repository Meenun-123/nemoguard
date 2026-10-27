import unittest
from ai.model_client import MockModelClient, NebiusModelClient

class TestModelClient(unittest.TestCase):
    def test_mock_model_client_generation(self):
        client = MockModelClient()
        messages = [
            {"role": "system", "content": "You are a test assistant"},
            {"role": "user", "content": "Analyze target code for security issues"}
        ]
        response = client.generate(messages)

        self.assertIn("content", response)
        self.assertIn("usage", response)
        self.assertGreater(response["usage"]["total_tokens"], 0)
        self.assertEqual(response["mode"], "mock_local")
        self.assertIn("Mock", response["model"])

    def test_nebius_client_missing_key_validation(self):
        with self.assertRaises(ValueError):
            NebiusModelClient(api_key="mock-key")

if __name__ == "__main__":
    unittest.main()
