import pandas as pd
import openpyxl as xl
import json

# file path
file_path = "D://Abdelrahman//Quick_Books_Project//acc_project//Files QuickBooks//ADVEC//05 May 2024 Advec.xlsx"

# Re-load the Excel file skipping the first 3 rows
df = pd.read_excel(file_path, skiprows=3)

# Drop any rows where all elements are NaN
df.dropna(how='all', inplace=True)

# Find the index where "Income" appears in the first column
income_index = df[df.iloc[:, 0] == 'Income'].index[0]

# Skip all rows before "Income"
df = df.iloc[income_index:]

# Rename the columns as "Category", "Total-1", "Total-2"
df.columns = ["Category", "Total-1", "Total-2"]

# Reset the index for the DataFrame
df.reset_index(drop=True, inplace=True)

# Display the first few rows to confirm
df.head()


# Initialize an empty list to hold the structured data
structured_data = []

# Initialize variables to keep track of the current parent and subparent
current_parent = None
current_subparent = None

# Iterate through the DataFrame to define the hierarchy
for index, row in df.iterrows():
    category = row["Category"].strip()
    total_1 = row["Total-1"]
    total_2 = row["Total-2"]
    
    # Treat "Gross Profit" and "Net Earnings" as parents regardless of totals
    if category in ["Gross Profit", "Net Earnings"] or (pd.isna(total_1) and pd.isna(total_2)):
        # It's a parent
        current_parent = {
            "category": category,
            "type": "parent",
            "children": []
        }
        structured_data.append(current_parent)
        current_subparent = None  # Reset subparent
        
        # Break the loop if "Net Earnings" is encountered
        if category == "Net Earnings":
            break
    elif pd.isna(total_1) and total_2 == 0:
        # It's a subparent under the current parent
        current_subparent = {
            "category": category,
            "type": "subparent",
            "children": []
        }
        if current_parent is not None:
            current_parent["children"].append(current_subparent)
    elif not pd.isna(total_1) and not pd.isna(total_2):
        # It's a child under the current parent or subparent
        child = {
            "category": category,
            "type": "child",
            "Total": total_1
        }
        if current_subparent is not None:
            current_subparent["children"].append(child)
        elif current_parent is not None:
            current_parent["children"].append(child)

# Save the structured data to a JSON file
import json

output_path = 'advec-structured_data.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

output_path
