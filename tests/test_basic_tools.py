import re
import unittest

from labs.lab05_tools_agents.basic_tools import is_now


class TestBasicTools(unittest.TestCase):
    def test_is_now_returns_vietnam_time_string(self):
        result = is_now.invoke({})

        self.assertIsInstance(result, str)
        self.assertRegex(
            result,
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} GMT\+7$",
        )


if __name__ == "__main__":
    unittest.main()
