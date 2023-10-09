snake_case_instruction = """Make sure that all field names are in SNAKE Case.
SNAKE Case means all field names are in LOWER CASE and spaces are converted to underscores(_) """

system_template_python_coder_load = """You are an expert Python programmer who produces detailed and well documented code."""
human_template_python_coder_load = """ Please generate Python Code to Load {excel} sheet into the {db} by creating a table with this name : {table_name}
Use the database connection as mentioned. 
Make sure that the connection is always made, use password provided {pwd}.

Example code:

import pandas as pd

# Load the Excel file
df = pd.read_excel('path')

# Convert field names to snake case
snake_case_columns = [col.lower().replace(' ', '_') for col in df.columns]
df.columns = snake_case_columns

# Create a table in the database
from sqlalchemy import create_engine

#Use the URI mentioned by the user
engine = create_engine('postgresql://postgres:12345@localhost:5432/test')

df.to_sql('employee', engine, if_exists='replace', index=False)
"""