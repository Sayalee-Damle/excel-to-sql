import tiktoken
from langchain.schema import Document
from typing import List
import create_table as ct
from pathlib import Path
from config import cfg


def num_tokens_from_data(doc: List[Document], table_name, headers,db):
    """Returns the number of tokens in a data"""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    document = []
    for val in doc:
        num_token += len(encoding.encode(val))
        if num_token < cfg.token_limit:
            document.append(val.split("\n\n\n"))
        else:
            insert_q = ct.insert_values(table_name=table_name, headers=headers, document=document)
            db.run(insert_q)
            num_tokens = 0