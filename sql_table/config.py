from pathlib import Path
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import SQLDatabase
import psycopg2
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType

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
    verbose_llm = os.getenv("VERBOSE_LLM") == "True"
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://postgres:12345@localhost/test",
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    token_limit = int(os.getenv("TOKEN_LIMIT"))
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
    python_executor = Path(os.getenv("PYTHON_SCRIPT"))

    #Database connection
    dbname = os.getenv("DB_NAME")
    user = os.getenv("USER")
    password = os.getenv("PWD")
    host = os.getenv("HOST")  # Usually 'localhost' if it's on your local machine
    port = os.getenv("PORT")  # Usually '5432' for PostgreSQL

# Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)


cfg = Config()


if __name__ == "__main__":
    print("llm: ", cfg.llm)
