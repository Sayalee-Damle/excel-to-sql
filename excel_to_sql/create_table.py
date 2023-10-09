from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from pathlib import Path
import psycopg2
from langchain.schema.messages import HumanMessage
from langchain.chains.openai_functions import create_structured_output_chain

from excel_to_sql.config import cfg 
from excel_to_sql.log_factory import logger
from excel_to_sql.model import PythonResponse
import excel_to_sql.templates as t

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

async def load_file(path: Path, db, table_name, pwd):
    chain = chain_factory_python_load()
    loader = await chain.arun({'excel': path, 'db': db, 'table_name': table_name, 'pwd': pwd})
    return loader.load_excel

async def python_executor(code):
    python_executor_dir = cfg.python_executor
    
    if not python_executor_dir.exists():
        python_executor_dir.mkdir(exist_ok=True, parents=True)

    executor_path = python_executor_dir / f"code_execution.py"
    with open(executor_path, 'w') as f:
        f.write(code)
    try:
        exec(open(executor_path).read())
        succesful_msg = "successful execution"
        logger.info(succesful_msg)
        return succesful_msg
    except:
        error_msg = "execution failed"
        logger.exception(error_msg)
        return error_msg

async def database_connection(db):
    conn = psycopg2.connect(dsn=db)
    return conn



if __name__ == "__main__":
    import asyncio
    db = asyncio.run(database_connection("postgresql://postgres:12345@localhost:5432/test"))
    table_name = "employee"
    path = Path(f"c:/Users/Sayalee/Documents/Employee Sample Data.xlsx")
    load_excel = asyncio.run(load_file(path, db, table_name, cfg.password))
    logger.info(load_excel)
    #logger.info(python_executor(load_excel))