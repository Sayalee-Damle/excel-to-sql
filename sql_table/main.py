import chainlit as cl
from chainlit.types import AskFileResponse
from pathlib import Path
import time

import psycopg2

async def ask_user_msg(question):
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(content=f"{question}").send()
    return ans

def database_connection(dbname, user, password, host, port):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return conn

@cl.on_chat_start
async def start() -> cl.Message:
    path_excel = await get_excel()
    await cl.Message(content=f"You will be asked questions related to the database where you want to create this table in.").send()
    db = await ask_user_msg("what is the database name?")
    user_name = await ask_user_msg("what is the user name associated with the database?")
    pwd = await ask_user_msg("what is the password associated with the given '{user_name}'?")
    host = await ask_user_msg("what is the host name?")
    port = await ask_user_msg("what is the port number?")
    


async def get_excel():
    files = None
    path_excel = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a excel file to begin!",
            accept=["application/excel"],
            max_files=1,
        ).send()
    path_excel = files[0]
    if not path_excel.exists():
        await cl.Message(content=f"File upload failed, restart the chat").send()
        return None

    return path_excel