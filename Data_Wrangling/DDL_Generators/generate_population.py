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
ddl_script += "    Population_id BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
ddl_script += "    County VARCHAR(25) NOT NULL,\n"
ddl_script += "    Population_Year YEAR NOT NULL,\n"
ddl_script += "    Age_Bracket VARCHAR(25) NOT NULL,\n"
ddl_script += "    Population_Total INT NOT NULL\n"
ddl_script += ");"

# Restructure age brackets strings to maintain consitency with prescription data
age_mapping = {
    '0-4': 'Ages 4 and younger',
    '5-17': 'Ages 5 To 17',
    '18-24': 'Ages 18 To 24',
    '25-34': 'Ages 25 To 34',
    '35-44': 'Ages 35 To 44',
    '45-54': 'Ages 45 To 54',
    '55-64': 'Ages 55 To 64',
    '65+': 'Ages 65 and older'
}

# Generate INSERT statements for data with age remapping
insert_statements = []
for row in data_rows:
    age_bracket = row[columns.index('Age_Bracket')]  # Get the age bracket from the row
    remapped_age = age_mapping.get(age_bracket, age_bracket)  # Use the mapping, or keep original if not found
    row[columns.index('Age_Bracket')] = remapped_age  # Update the age bracket in the row

    values = ", ".join([f"'{value}'" if column != "Population_Year" and column != "Population_Total" else value for column, value in zip(columns, row)])
    insert_statement = f"INSERT INTO {table_name} (County, Population_Year, Age_Bracket, Population_Total) VALUES ({values});"
    insert_statements.append(insert_statement)

# Write DDL and INSERT scripts to file
sql_filename = 'Data_Wrangling/Raw_SQL_Files/ALL_Population.SQL'

with open(sql_filename, 'w') as sql_file:
    sql_file.write(ddl_script + '\n\n')
    for insert_statement in insert_statements:
        sql_file.write(insert_statement + '\n')

    print(f"SQL script written to {sql_filename}")
