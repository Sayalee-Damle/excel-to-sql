import chainlit as cl
from chainlit.types import AskFileResponse
from pathlib import Path

import excel_to_sql.create_table as ct
from excel_to_sql.config import cfg


def write_to_disc(file) -> Path:
    path = cfg.path_excel / f"excel.xlsx"
    with open(path, 'wb') as f:
        f.write(file.content)
    return path

async def delete_excel():
    path = cfg.path_excel / f"excel.xlsx"
    Path.unlink(path)

@cl.on_chat_start
async def start() -> cl.Message:
    path_excel = await get_excel()
    if path_excel:
        await cl.Message(content=f"You will be asked questions related to the database where you want to create this table in.").send()
        conn = cfg.conn
        password = cfg.password
        table_name = await ask_user_msg("what do you want the table name to be?")
        excel_load = await ct.load_file(path_excel, conn, table_name['content'], password)
        code_run = await ct.python_executor(excel_load)
        if code_run == 'successful execution':
            await cl.Message(content=f"Table Created").send()    
        else:
            await cl.Message(content=f"Some error occured").send()
            
        await delete_excel()
        return
    
async def ask_user_msg(question)-> AskFileResponse:
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(content=f"{question}", timeout=cfg.ui_timeout).send()
    return ans

async def get_excel():
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a excel file to begin!",
            accept=["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
            max_files=1,
        ).send()
    path_excel = write_to_disc(files[0])
    return path_excel

