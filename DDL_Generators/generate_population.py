import csv

# Read CSV file and extract column names and data rows
csv_filename = 'Processed_Data/Population_Data'

with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    columns = next(csv_reader)
    data_rows = list(csv_reader)

# Generate DDL script
table_name = 'Population'

ddl_script = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
ddl_script += "    id BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
ddl_script += "    County VARCHAR(255) NOT NULL,\n"
ddl_script += "    Year INT NOT NULL,\n"
ddl_script += "    Age_Bracket VARCHAR(255) NOT NULL,\n"
ddl_script += "    Population_Total INT NOT NULL\n"
ddl_script += ");"

# Generate INSERT statements for data
insert_statements = []
for row in data_rows:
    values = ", ".join([f"'{value}'" if column != "Year" and column != "Population_Total" else value for column, value in zip(columns, row)])
    insert_statement = f"INSERT INTO {table_name} (County, Year, Age_Bracket, Population_Total) VALUES ({values});"
    insert_statements.append(insert_statement)

# Write DDL and INSERT scripts to file
sql_filename = 'Raw_SQL_Files/ALL_Population.SQL'

with open(sql_filename, 'w') as sql_file:
    sql_file.write(ddl_script + '\n\n')
    for insert_statement in insert_statements:
        sql_file.write(insert_statement + '\n')

    print(f"SQL script written to {sql_filename}")
