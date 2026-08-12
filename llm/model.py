from dotenv import load_dotenv

import os

from langchain_ollama import ChatOllama


load_dotenv()


MODEL_NAME = os.getenv("OLLAMA_MODEL")


def get_llm():

    return ChatOllama(

        model=MODEL_NAME,

        temperature=0

    )