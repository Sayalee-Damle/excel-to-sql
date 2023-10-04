from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import SQLDatabase
import psycopg2

load_dotenv()


class Config:
    model_name = os.getenv("OPENAI_MODEL")
    llm_cache = os.getenv("LLM_CACHE") == "True"
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model_name,
        temperature=0,
        request_timeout=os.getenv("REQUEST_TIMEOUT"),
        cache=llm_cache,
        streaming=True,
    )
    verbose_llm = os.getenv("VERBOSE_LLM") == "False"
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://postgres:12345@localhost/test",
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    token_limit = int(os.getenv("TOKEN_LIMIT"))


cfg = Config()


if __name__ == "__main__":
    print("llm: ", cfg.llm)
