import os

from crewai import LLM


class LlmHelper:

    def llamaConnection():

        # Load LLM configuration for Ollama model
        llm = LLM(

            base_url=os.getenv("LLAMA_BASE_URL"),
            model=os.getenv("LLAMA_MODEL")
        )

        return llm

    def GeminiConnection():
        llm = LLM(

            model=os.getenv("GEMINI_MODEL"),
            api_key=os.getenv("GEMINI_API_KEY"),
            # base_url="https://generativelanguage.googleapis.com"
        )

        return llm

