import os
from crewai import LLM
import toml

config = toml.load("secrets.toml")


class LlmHelper:

    # Define the LLM connection
    def llamaConnection():
        llm = LLM(
            base_url=config["LLAMA_BASE_URL"],
            model=config["LLAMA_MODEL"]
        )
        return llm
    
    # Define the Gemini connection
    def GeminiConnection():
        llm = LLM(
            model=config["GEMINI_MODEL"],
            api_key=config["GEMINI_API_KEY"],
        )
        return llm

