# THIS FILE SHOULD ALSO BE CHECKING FOR BAD DATA (E.G. Null values or non-integer values for specific columns)

import os
import pandas as pd
from pathlib import Path


def process_file(file_path, age_bracket_mapping):
    """
    Process a single data file to create a DataFrame with relevant information.

    Args:
        file_path (str): Path to the data file.
        age_bracket_mapping (dict): Mapping of age brackets to desired age brackets.

    Returns:
        pandas.DataFrame: Processed DataFrame containing age bracket, county, year, and population data.
    """
    df = pd.read_csv(file_path)

    # Filter out rows with County = "Michigan"
    df = df[df["County"] != "Michigan"]

    # Select and rename columns
    if "Kids.csv" in file_path:
        age_col_indices = [0, 4, 6]
    elif "Younger_Adults.csv" in file_path:  # Younger_Adults.csv
        age_col_indices = [0, 4, 6, 8, 10, 12, 14]
    else:  # Older_Adults.csv
        age_col_indices = [0, 4, 6, 8, 10, 12]

    if "Kids.csv" in file_path:
        age_brackets = ["<1", "1-4"]
    elif "Younger_Adults.csv" in file_path:
        age_brackets = ["18-19", "20-24", "25-29", "30-34", "35-39", "40-44"]
    else:  # Older_Adults.csv
        age_brackets = ["45-49", "50-54", "55-59", "60-64", "65+"]

    df = df.iloc[:, age_col_indices]
    df.columns = ["County"] + age_brackets

    # Convert Population_Total column to integers
    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", "").astype(int)

    # Add the "Year" column
    year = os.path.basename(os.path.dirname(file_path))
    df["Year"] = year

    # Melt the dataframe to have Age-Bracket as a column
    df_melted = pd.melt(
        df,
        id_vars=["County", "Year"],
        var_name="Age_Bracket",
        value_name="Population_Total"
    )

    # Apply age bracket mapping
    df_melted["Age_Bracket"] = df_melted["Age_Bracket"].apply(
        lambda x: age_bracket_mapping.get(x, x)
    )

    # Group by County, Year, and Age-Bracket and sum Population_Total
    df_grouped = df_melted.groupby(
        ["County", "Year", "Age_Bracket"],
        as_index=False
    )["Population_Total"].sum()

    return df_grouped


def process_directory(data_dir, age_bracket_mapping):
    """
    Process a directory of data files to create a final combined DataFrame.

    Args:
        data_dir (str): Path to the directory containing data files.
        age_bracket_mapping (dict): Mapping of age brackets to desired age brackets.

    Returns:
        pandas.DataFrame: Combined DataFrame containing processed data.
    """
    processed_dfs = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file in ["Kids.csv", "Younger_Adults.csv", "Older_Adults.csv"]:
                file_path = os.path.join(root, file)
                df_processed = process_file(file_path, age_bracket_mapping)
                processed_dfs.append(df_processed)

    final_df = pd.concat(processed_dfs, ignore_index=True)
    return final_df


# Path to Raw_Data directory
data_dir = Path("Raw_Data/Population_Data")

# Define age brackets mapping
age_bracket_mapping = {
    "<1": "0-4",
    "1-4": "0-4",
    "5-9": "5-17",
    "10-14": "5-17",
    "15-17": "5-17",
    "18-19": "18-24",
    "20-24": "18-24",
    "25-29": "25-34",
    "30-34": "25-34",
    "35-39": "35-44",
    "40-44": "35-44",
    "45-49": "45-54",
    "50-54": "45-54",
    "55-59": "55-64",
    "60-64": "55-64",
    "65+": "65+"
}

# Process the directory and get the final dataframe
final_df = process_directory(data_dir, age_bracket_mapping)

# Save the final dataframe as a CSV file
final_df.to_csv(Path("Processed_Data/Population_Data"), index=False)
