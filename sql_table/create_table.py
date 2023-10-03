
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredExcelLoader
from pathlib import Path
from model import SQLResponse

import templates as t
from config import cfg
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.schema import Document
from typing import List
from langchain.chains.openai_functions import create_structured_output_chain


def prompt_factory(system_template, human_template):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template= system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(template= human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    return chat_prompt

def chain_factory_SQL_insert() -> LLMChain:
    return create_structured_output_chain(
        SQLResponse,
        cfg.llm,
        prompt_factory(t.sys_template_data_loader_1,t.human_template_data_loader_1),
        verbose=cfg.verbose_llm,
    )

def chain_factory_SQL_create() -> LLMChain:
    return create_structured_output_chain(
        SQLResponse,
        cfg.llm,
        prompt_factory(t.system_template_create,t.human_template_create),
        verbose=cfg.verbose_llm,
    )

def chain_factory_excel_extract() -> LLMChain:
    return create_structured_output_chain(
        str,
        cfg.llm,
        prompt_factory(t.system_template_create,t.human_template_create),
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


def create_table(header_type, db, table_name):
    prompt_factory(t.system_template_create, t.human_template_create)
    chain = chain_factory_SQL_create()
    create_q: SQLResponse = chain.run({'table_name': table_name, 'db': db, 'header_type': header_type})
    return create_q

def insert_values(table_name, headers, document):
    prompt_factory(t.sys_template_data_loader_1, t.human_template_data_loader_1)
    chain = chain_factory_SQL_insert()
    query: SQLResponse = chain.run({'table_name': table_name, 'headers': headers, 'docs': document})
    return query.insert_sql

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
    document = []
    for doc in docs:
        document.append(doc.page_content.split("\n\n\n"))
    document = document[0]
    #print(document)
    header_type = extract_keys(docs)
    #print(header_type)
    #create_q = create_table(header_type, db, 'finance')
    #db.run(create_q)
    insert_q = insert_values(table_name='finance', headers=header_type, document=document)
    print(insert_q)