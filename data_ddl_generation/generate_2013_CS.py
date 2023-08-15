import pandas as pd
from pathlib import Path

# Read the Excel file
excel_file = pd.ExcelFile(Path('Raw_Data/CS_Data/2013/Drug Utilization Report Data - 2013.xlsx'))

# Define the worksheet names
worksheets = ['PRESCRIBER COUNTY', 'PATIENT COUNTY']

# Initialize a list to store DataFrames
dataframes = []

# Iterate through worksheets
for sheet_name in worksheets:
    df = excel_file.parse(sheet_name)

    # Exclude the last row (summary row) from each worksheet
    df = df.iloc[:-1]

    dataframes.append(df)

# Combine DataFrames
combined_data = pd.concat(dataframes, ignore_index=True)

# Add a new column for Year
combined_data['Year'] = 2013

# Add columns with NULL values
# null_columns = ['Total_Patients', 'Total_Days_Supply', 'Average_Daily_MME', 'Total_Above_90MME']
# for col in null_columns:
#     combined_data[col] = None

# Rename columns for SQL generation
column_mapping = {
    'PRESCRIPTION COUNT (#)': 'Prescription_Count',
    'PRESCRIPTION QUANTITY (#)': 'Prescription_Quantity',
    'DEA DRUG SCHEDULE': 'DEA_Drug_Schedule'
}

combined_data.rename(columns=column_mapping, inplace=True)

# Define the output SQL file path
output_sql_file = 'SQL_Files/2013_CS.SQL'

# Generate DDL SQL statements
ddl_statements = [
    "CREATE TABLE IF NOT EXISTS Prescription_Data (",
    "Prescription_Category_ID INT PRIMARY KEY AUTO_INCREMENT,",
    "Year YEAR,",
    "Patient_County VARCHAR(255),",
    "Patient_State VARCHAR(255),",
    "Prescriber_County VARCHAR(255),",
    "Prescriber_State VARCHAR(255),",
    "Drug_Name/Strength VARCHAR(255),",
    "DEA_Drug_Schedule INT,",
    "AHFS_Description VARCHAR(255),",
    "Prescription_Count INT,",
    "Prescription_Quantity INT,",
    "Total_Patients INT,",
    "Total_Days_Supply INT,",
    "Average_Daily_MME INT,",
    "Total_Above_90MME INT",
    ");"
]

# Generate INSERT SQL statements
insert_statements = []
for index, row in combined_data.iterrows():
    insert_values = [
        '2013',
        f"'{row.get('PATIENT COUNTY')}'" if pd.notna(row.get('PATIENT COUNTY')) else 'NULL', # Handle the case where the column doesn't exist
        f"'{row.get('PATIENT STATE')}'" if pd.notna(row.get('PATIENT STATE')) else 'NULL', # Handle the case where the column doesn't exist
        f"'{row.get('PRESCRIBER COUNTY')}'" if pd.notna(row.get('PRESCRIBER COUNTY')) else 'NULL', # Handle the case where the column doesn't exist
        f"'{row.get('PRESCRIBER STATE')}'" if pd.notna(row.get('PRESCRIBER STATE')) else 'NULL', # Handle the case where the column doesn't exist
        f"'{row.get('DRUG NAME/STRENGTH')}'",
        f"'{row.get('DEA_Drug_Schedule')}'",
        f"'{row.get('AHFS DESCRIPTION')}'",
        f"{row.get('Prescription_Count')}",
        f"{row.get('Prescription_Quantity')}",
        'NULL',  # For Total_Patients
        'NULL',  # For Total_Days_Supply
        'NULL',  # For Average_Daily_MME
        'NULL'   # For Total_Above_90MME
    ]

    insert_statement = f"INSERT INTO Prescription_Data (Year, Patient_County, Patient_State, Prescriber_County, Prescriber_State, "
    insert_statement += f"Drug_Name/Strength, DEA_Drug_Schedule, AHFS_Description, Prescription_Count, Prescription_Quantity, "
    insert_statement += f"Total_Patients, Total_Days_Supply, Average_Daily_MME, Total_Above_90MME) VALUES "
    insert_statement += f"({', '.join(insert_values)});"

    insert_statements.append(insert_statement)

# Write DDL, INSERT, and validation error statements to the output SQL file
with open(output_sql_file, 'w') as sql_file:
    sql_file.write('\n'.join(ddl_statements))
    sql_file.write('\n')
    sql_file.write('\n'.join(insert_statements))

print(f"DDL, INSERT, and validation error statements generated and saved to {output_sql_file}")
