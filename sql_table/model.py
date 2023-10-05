from pydantic import BaseModel
from pydantic import Field
from typing import Optional


class SQLResponse(BaseModel):
    """Contains a SQL Query """
    insert_sql : Optional[str] = Field(
        ...,
        description = "sql insert query used to insert data from the .xlsx sheet into the table created "
    )

    create_sql : Optional[str] = Field(
        ...,
        description = "sql create query used to create table from the column names extracted from the .xlsx file "
    )

class PythonResponse(BaseModel):
    """Contains Python Code"""
    load_excel : Optional[str] = Field(
        ...,
        description = "Python Code to load excel sheet into given database"
    )