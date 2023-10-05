import pandas as pd

# Load the Excel file
path = 'c:\\Users\\Sayalee\\Documents\\Employee Sample Data.xlsx'
df = pd.read_excel(path)

# Convert field names to snake case
snake_case_columns = [col.lower().replace(' ', '_') for col in df.columns]
df.columns = snake_case_columns

# Create a table in the database
from sqlalchemy import create_engine

# Replace 'xxx' with the actual password
engine = create_engine('postgresql://postgres:12345@localhost:5432/test')

df.to_sql('employee', engine, if_exists='replace', index=False)