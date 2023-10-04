
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredExcelLoader
from pathlib import Path
import tiktoken
from model import SQLResponse
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
import supportfuncs as sf
from log_factory import logger



def prompt_factory(system_template, human_template, add_snake_case = False):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template= system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(template= human_template)
    messages = [system_message_prompt, human_message_prompt] 
    if add_snake_case:
        messages.append(HumanMessage(content=t.snake_case_instruction))
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    return chat_prompt

def chain_factory_SQL_insert() -> LLMChain:
    return create_structured_output_chain(
        SQLResponse,
        cfg.llm,
        prompt_factory(t.sys_template_data_loader_1,t.human_template_data_loader_1, True),
        verbose=cfg.verbose_llm,
    )

def chain_factory_SQL_create() -> LLMChain:
    return create_structured_output_chain(
        SQLResponse,
        cfg.llm,
        prompt_factory(t.system_template_create,t.human_template_create, False),
        verbose=cfg.verbose_llm,
    )

def chain_factory_excel_extract() -> LLMChain:
    return create_structured_output_chain(
        str,
        cfg.llm,
        prompt_factory(t.sys_template_loader,t.human_template_loader),
        verbose=cfg.verbose_llm,
    )
def excel_loader(path: Path) -> List[Document]:
    loader = UnstructuredExcelLoader(path, mode = "elements")
    docs = loader.load_and_split()
    return docs

def extract_keys(doc: any) -> str:
    prompt_factory(t.sys_template_loader,t.human_template_loader)
    chain = chain_factory_excel_extract()
    headers: str = chain.run({'doc': doc})
    return headers

def get_col_names(table_name:str, db):
    q = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;"
    print(q)
    col_names = db.run(q)
    return col_names

def create_table(header_type, db, table_name):
    chain = chain_factory_SQL_create()
    create_q: SQLResponse = chain.run({'table_name': table_name, 'db': db, 'header_type': header_type})
    return create_q

def insert_values(table_name, headers, document):
    prompt_factory(t.sys_template_data_loader_1, t.human_template_data_loader_1)
    chain = chain_factory_SQL_insert()
    query: SQLResponse = chain.run({'table_name': table_name, 'headers': headers, 'docs': document})
    return query.insert_sql

def num_tokens_from_data(doc: List[Document], table_name: str, headers, db):
    print("in num tokens")
    encoding = tiktoken.encoding_for_model(cfg.model_name)
    num_tokens = 0
    document = []
    for val in doc:
        num_tokens += len(encoding.encode(val.page_content))
        if num_tokens < cfg.token_limit:
            document.append(val.page_content.split("\n\n\n"))
        else:
            execute_query(table_name, headers, db, document)  
            num_tokens = 0
            document = []
    execute_query(table_name, headers, db, document) 

def execute_query(table_name, headers, db, document):
    insert_q = insert_values(table_name=table_name, headers=headers, document=document[0])
    logger.info(insert_q)
    db.run(insert_q)  

if __name__ == "__main__":
    db = cfg.db
    agent_executor = create_sql_agent(
        llm=cfg.llm,
        toolkit=cfg.toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
    path = Path(f"C:/Users/Sayalee/Downloads/Financial Sample.xlsx")
    docs = excel_loader(path)
    document = docs
    header_type = extract_keys(docs)
    col_names = get_col_names('finance', db)
    #create_q = create_table(col_names, db, 'finance')
    #print(create_q)
    num_tokens_from_data(document, 'finance',col_names, db)
    
    #print(document)
    #print(header_type)
    
    #db.run(create_q)
    #print(get_col_names())