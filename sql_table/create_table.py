
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredExcelLoader
from pathlib import Path

import templates as t
from config import cfg
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.schema import Document
from typing import List

def excel_loader(path: Path) -> List[Document]:
    loader = UnstructuredExcelLoader(path, mode = "elements")
    docs = loader.load()
    return docs[0].page_content

def extract_keys(doc: any) -> dict:
    system_message_prompt = SystemMessagePromptTemplate.from_template(template= t.sys_template_loader)
    human_message_prompt = HumanMessagePromptTemplate.from_template(t.human_template_loader)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm = cfg.llm, prompt = chat_prompt)
    headers = chain.run({'doc': doc})
    return headers

def create_table(header_type, db, table_name):
    system_message_prompt = SystemMessagePromptTemplate.from_template(t.system_template_create)
    human_message_prompt = HumanMessagePromptTemplate.from_template(t.human_template_create)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm = cfg.llm, prompt = chat_prompt)
    create_q = chain.run({'table_name': table_name, 'db': db, 'header_type': header_type})
    db.run(create_q)

if __name__ == "__main__":
    db = cfg.db
    
    
    agent_executor = create_sql_agent(
    llm=cfg.llm,
    toolkit=cfg.toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
    path = Path(f"C:/Users/Sayalee/Downloads/Financial Sample.xlsx")
    doc = excel_loader(path)
    #print(doc)
    header_type = extract_keys(doc)
    #print(header_type)
    #create_table(header_type)
    system_message_prompt = SystemMessagePromptTemplate.from_template(t.sys_template_data_loader)
    human_message_prompt = HumanMessagePromptTemplate.from_template(t.human_template_data_loader)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm = cfg.llm, prompt = chat_prompt)
    print(chain.run({'doc': doc}))