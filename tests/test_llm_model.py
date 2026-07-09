import sys
import types
import unittest

from labs.lab01_foundation.llm_model import LLMModel
from shared.config import settings


class FakeChatGroq:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class TestLLMModel(unittest.TestCase):
    def test_groq_chat_uses_settings_and_caches_instance(self):
        fake_module = types.ModuleType("langchain_groq")
        fake_module.ChatGroq = FakeChatGroq
        previous_module = sys.modules.get("langchain_groq")
        sys.modules["langchain_groq"] = fake_module

        model = LLMModel.__new__(LLMModel)
        model.groq_llm = None

        try:
            groq_llm = model.groq_chat()
            self.assertIs(groq_llm, model.groq_llm)
            self.assertEqual(groq_llm.kwargs["model"], "llama-3.1-8b-instant")
            self.assertEqual(groq_llm.kwargs["api_key"], settings.GROQ_API_KEY)

            cached_llm = model.groq_chat()
            self.assertIs(cached_llm, groq_llm)
        finally:
            if previous_module is None:
                del sys.modules["langchain_groq"]
            else:
                sys.modules["langchain_groq"] = previous_module


if __name__ == "__main__":
    unittest.main()
