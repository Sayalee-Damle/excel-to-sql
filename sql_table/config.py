from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import SQLDatabase
import psycopg2

load_dotenv()

class Config:
    model = os.getenv("OPENAI_MODEL")
    llm = OpenAI(temperature=0)
    db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:12345@localhost/test",
)
    toolkit = SQLDatabaseToolkit(db=db, llm = llm)

    
    
cfg = Config()


if __name__ == "__main__":
    print("llm: ", cfg.llm)