import unittest

from labs.lab05_tools_agents.create_agent import run_agent_query


class FakeAgent:
    def __init__(self):
        self.received_payload = None

    async def ainvoke(self, payload):
        self.received_payload = payload
        return {"messages": ["ok"]}


class TestCreateAgentAsync(unittest.IsolatedAsyncioTestCase):
    async def test_run_agent_query_uses_async_agent_invocation(self):
        agent = FakeAgent()

        result = await run_agent_query(agent, "Tinh 2+3")

        self.assertEqual(result, {"messages": ["ok"]})
        self.assertEqual(
            agent.received_payload,
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Tinh 2+3",
                    }
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
