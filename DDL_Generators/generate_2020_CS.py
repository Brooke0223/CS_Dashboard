import pandas as pd
from pathlib import Path

# Read the Excel file
excel_file = pd.ExcelFile(Path('Raw_Data/CS_Data/2020/2020_Michigan_Drug_Utilization_Report_FINAL.xlsx'))

# Define the worksheet names
worksheets = ['Prescriber County', 'Patient County']

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
combined_data['Prescription_Year'] = 2020

# Define column name mapping
column_mapping = {
    'PRESCRIPTION COUNT': 'Total_Prescriptions',
    'PRESCRIPTION QUANTITY (DOSAGE UNITS)': 'Total_Units',
    'DRUG SCHEDULE': 'DEA_Drug_Schedule',
    'DRUG NAME/STRENGTH': 'Drug_Name_Strength',
    'AGE RANGE': 'Patient_Age_Bracket',
    'PATIENT COUNT': 'Total_Patients',
    'DAYS SUPPLY': 'Total_Days_Supply',
    'AVERAGE DAILY MMEs (*ONLY CALCULATED FOR OPIATE AGONISTS AND OPIATE PARTIAL AGONISTS)': 'Average_Daily_MME',
    'PRESCRIPTION COUNT GREATER THAN OR EQUAL TO 90 MMEs (*ONLY CALCULATED FOR OPIATE AGONISTS AND OPIATE PARTIAL AGONISTS)': 'Total_Above_90MME'
}

# Rename columns
combined_data.rename(columns=column_mapping, inplace=True)

# Map 2-letter state abbreviation data to the full state names
state_mapping = {
    'AL': 'ALABAMA',
    'AK': 'ALASKA',
    'AZ': 'ARIZONA',
    'AR': 'ARKANSAS',
    'CA': 'CALIFORNIA',
    'CO': 'COLORADO',
    'CT': 'CONNECTICUT',
    'DE': 'DELAWARE',
    'FL': 'FLORIDA',
    'GA': 'GEORGIA',
    'HI': 'HAWAII',
    'ID': 'IDAHO',
    'IL': 'ILLINOIS',
    'IN': 'INDIANA',
    'IA': 'IOWA',
    'KS': 'KANSAS',
    'KY': 'KENTUCKY',
    'LA': 'LOUISIANA',
    'ME': 'MAINE',
    'MD': 'MARYLAND',
    'MA': 'MASSACHUSETTS',
    'MI': 'MICHIGAN',
    'MN': 'MINNESOTA',
    'MS': 'MISSISSIPPI',
    'MO': 'MISSOURI',
    'MT': 'MONTANA',
    'NE': 'NEBRAKSA',
    'NV': 'NEVADA',
    'NH': 'NEW HAMPSHIRE',
    'NJ': 'NEW JERSEY',
    'NM': 'NEW MEXICO',
    'NY': 'NEW YORK',
    'NC': 'NORTH CAROLINA',
    'ND': 'NORTH DAKOTA',
    'OH': 'OHIO',
    'OK': 'OKLAHOMA',
    'OR': 'OREGON',
    'PA': 'PENNSYLVANIA',
    'PR': 'PUERTO RICO',
    'RI': 'RHODE ISLAND',
    'SC': 'SOUTH CAROLINA',
    'SD': 'SOUTH DAKOTA',
    'TN': 'TENNESSEE',
    'TX': 'TEXAS',
    'UT': 'UTAH',
    'VT': 'VERMONT',
    'VA': 'VIRGINIA',
    'WA': 'WASHINGTON',
    'WV': 'WEST VIRGINIA',
    'WI': 'WISCONSIN',
    'WY': 'WYOMING'
}
combined_data['PATIENT STATE'] = combined_data['PATIENT STATE'].replace(state_mapping)
combined_data['PRESCRIBER STATE'] = combined_data['PRESCRIBER STATE'].replace(state_mapping)

# Initialize a list to track validation errors
validation_errors = []

# Perform data validation
for index, row in combined_data.iterrows():
    try:
        pd.to_numeric(row['Total_Prescriptions'])
        pd.to_numeric(row['Total_Units'])
        pd.to_numeric(row['DEA_Drug_Schedule'][-1])
    except ValueError as e:
        validation_errors.append(f"Validation error at row {index + 2}: {e}")


# Convert selected columns to integers
def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None


integer_columns = ['Total_Prescriptions', 'Total_Units', 'Total_Patients', 'Total_Days_Supply']
for col in integer_columns:
    combined_data[col] = combined_data[col].apply(convert_to_int)

# Convert DEA_Drug_Schedule values to integer by taking the last character
combined_data['DEA_Drug_Schedule'] = combined_data['DEA_Drug_Schedule'].apply(lambda x: int(str(x)[-1]))

# Define the output SQL file path
output_sql_file = 'Raw_SQL_Files/2020_CS.SQL'

# Generate DDL SQL statements
ddl_statements = [
    "CREATE TABLE IF NOT EXISTS Prescription_Data (",
    "Prescription_Category_ID INT PRIMARY KEY AUTO_INCREMENT,",
    "Prescription_Year YEAR,",
    "Prescriber_County VARCHAR(255),",
    "Prescriber_State VARCHAR(255),",
    "Patient_County VARCHAR(255),",
    "Patient_State VARCHAR(255),",
    "Patient_Age_Bracket VARCHAR(255),",
    "Drug_Name_Strength VARCHAR(255),",
    "DEA_Drug_Schedule INT,",
    "AHFS_Description VARCHAR(255),",
    "Total_Prescriptions INT,",
    "Total_Units INT,",
    "Total_Patients INT,",
    "Total_Days_Supply INT,",
    "Average_Daily_MME FLOAT,",
    "Total_Above_90MME INT",
    ");"
]

# Generate INSERT SQL statements
insert_statements = []
for index, row in combined_data.iterrows():
    insert_values = [
        '2020',
        f"'{row.get('PRESCRIBER COUNTY')}'" if pd.notna(row.get('PRESCRIBER COUNTY')) else 'NULL',  # Handle case where column doesn't exist
        f"'{row.get('PRESCRIBER STATE')}'" if pd.notna(row.get('PRESCRIBER STATE')) else 'NULL',  # Handle case where column doesn't exist
        f"'{row.get('PATIENT COUNTY')}'" if pd.notna(row.get('PATIENT COUNTY')) else 'NULL',  # Handle case where column doesn't exist
        f"'{row.get('PATIENT STATE')}'" if pd.notna(row.get('PATIENT STATE')) else 'NULL',  # Handle case where column doesn't exist
        f"'{row.get('Patient_Age_Bracket')}'",
        f"'{row.get('Drug_Name_Strength')}'",
        f"{row.get('DEA_Drug_Schedule')}",
        f"'{row.get('AHFS DESCRIPTION')}'",
        f"{row.get('Total_Prescriptions')}",
        f"{row.get('Total_Units')}",
        f"{row.get('Total_Patients')}",
        f"{row.get('Total_Days_Supply')}",
        f"{row.get('Average_Daily_MME')}" if pd.notna(row.get('Average_Daily_MME')) else 'NULL',  # Handle case where column is N/A
        f"{int(row.get('Total_Above_90MME'))}" if pd.notna(row.get('Total_Above_90MME')) else 'NULL'  # Handle case where column is N/A
    ]

    insert_statement = "INSERT INTO Prescription_Data (Prescription_Year, Prescriber_County, Prescriber_State, Patient_County, Patient_State, Patient_Age_Bracket, "
    insert_statement += "Drug_Name_Strength, DEA_Drug_Schedule, AHFS_Description, Total_Prescriptions, Total_Units, "
    insert_statement += "Total_Patients, Total_Days_Supply, Average_Daily_MME, Total_Above_90MME) VALUES "
    insert_statement += f"({', '.join(insert_values)});"

    insert_statements.append(insert_statement)

# Write DDL, INSERT, and validation error statements to the output SQL file
with open(output_sql_file, 'w') as sql_file:
    sql_file.write('\n'.join(ddl_statements))
    sql_file.write('\n')
    sql_file.write('\n'.join(insert_statements))

print(f"DDL, INSERT, and validation error statements generated and saved to {output_sql_file}")
