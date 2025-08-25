import logging
import os
from enum import Enum

from dotenv import find_dotenv, load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ProductEnum(str, Enum):
    EduTrack = "EduTrack"
    TuneHive = "TuneHive"


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


def load_env():
    env_path = find_dotenv()
    if not env_path:
        raise FileNotFoundError(
            "No .env file found. Please create one with your OPENAI_API_KEY."
        )
    load_dotenv(env_path)

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    if langchain_api_key:
        os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

    langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
    if langchain_tracing_v2:
        os.environ["LANGCHAIN_TRACING_V2"] = langchain_tracing_v2

    langchain_project = os.getenv("LANGCHAIN_PROJECT")
    if langchain_project:
        os.environ["LANGCHAIN_PROJECT"] = langchain_project

    docs_base_path = os.path.join(ROOT_DIR, "data")
    vector_store_path = os.path.join(docs_base_path, "vector_store")
    os.environ["DOCS_BASE_PATH"] = os.getenv("DOCS_BASE_PATH", docs_base_path)
    os.environ["VECTOR_STORE_PATH"] = os.getenv("VECTOR_STORE_PATH", vector_store_path)


def get_llm(**kwargs):
    load_env()
    if "OPENAI_API_KEY" in os.environ:
        return ChatOpenAI(model="gpt-4o", temperature=1, top_p=1.0, n=1, **kwargs)
    else:
        return ChatOllama(model="llama3.2", temperature=1, **kwargs)


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
