from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredExcelLoader
from pathlib import Path
import psycopg2
import tiktoken
from model import SQLResponse, PythonResponse
from langchain.schema.messages import HumanMessage
import templates as t
from config import cfg
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.schema import Document
from typing import List
from langchain.chains.openai_functions import create_structured_output_chain

from log_factory import logger

def prompt_factory(system_template, human_template, add_snake_case = False):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template= system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(template= human_template)
    messages = [system_message_prompt, human_message_prompt] 
    if add_snake_case:
        messages.append(HumanMessage(content=t.snake_case_instruction))
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    return chat_prompt

def chain_factory_python_load() -> LLMChain:
    return create_structured_output_chain(
        PythonResponse,
        cfg.llm,
        prompt_factory(t.system_template_python_coder_load,t.human_template_python_coder_load, True),
        verbose=cfg.verbose_llm,
    )

def load_file(path: Path, db, table_name, pwd):
    chain = chain_factory_python_load()
    loader = chain.run({'excel': path, 'db': db, 'table_name': table_name, 'pwd': pwd})
    return loader.load_excel

def python_executor(code):
    python_executor_dir = cfg.python_executor
    # used to create embeddings
    if not python_executor_dir.exists():
        python_executor_dir.mkdir(exist_ok=True, parents=True)

    executor_path = python_executor_dir / f"code_execution.py"
    with open(executor_path, 'w') as f:
        f.write(code)
    try:
        exec(open(executor_path).read())
        succesful_msg = "successful execution"
        return succesful_msg
    except:
        error_msg = "execution failed"
        return error_msg




if __name__ == "__main__":
    db = cfg.conn
    table_name = "employee"
    path = Path(f"c:/Users/Sayalee/Documents/Employee Sample Data.xlsx")
    load_excel = load_file(path, db, table_name, cfg.password)
    logger.info(load_excel)
    logger.info(python_executor(load_excel))