sys_template_loader = "You are excel loader"
human_template_loader = "You will extract the zeroth row with headers from the {doc} and return the keys and find out the data type. Display in form of a dictionary"

system_template_create = "you create SQL tables in database"
human_template_create = """Create a table {table_name} using {header_type} with the specified data type in {db}. Use Create statement with if not exists."""

sys_template_data_loader = "You will load the data from excel file"
human_template_data_loader = """"convert {doc} into tuples of data.
"""
sys_template_data_loader_1 = "You are an expert SQL coder"
human_template_data_loader_1 = """" Please generate a sql query to insert data into {table_name} using {headers} with these values = {docs}
Example of the query:
INSERT INTO {table_name} {headers} values {docs};
"""