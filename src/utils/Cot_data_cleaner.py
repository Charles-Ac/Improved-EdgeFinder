"""
This script processes a COT (Commitment of Traders) data CSV file by performing the following operations:
1. Filters the data to only include rows from the current year.
2. Sorts the data by 'Contract Name' and 'Date' in descending order.
3. Calculates the percentage of long and short positions relative to the total contracts.
4. Calculates the net percentage change in long positions compared to the previous week's data.
5. Ensures short positions are positive values and reorders the columns.
6. Saves the cleaned data into a new CSV file.
"""

import pandas as pd

# Function to calculate net percentage change
def calculate_net_percentage_change(current_long, current_short, previous_long, previous_short):
    current_short = abs(current_short)
    previous_short = abs(previous_short)
    current_long_percentage = current_long / (current_long + current_short)
    previous_long_percentage = previous_long / (previous_long + previous_short)
    net_percentage_change = (current_long_percentage - previous_long_percentage) * 100  # Convert to percentage
    return round(net_percentage_change, 2)

# Load the CSV file into a DataFrame
df = pd.read_csv('cot-reports.csv')

# Ensure 'Date' is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter the data to only include rows from the current year (2024)
df = df[df['Date'].dt.year == 2024]

# Sort the data by 'Contract Name' and 'Date' in descending order
df = df.sort_values(by=['Contract Name', 'Date'], ascending=[True, False])

# Initialize an empty list to store the final rows
final_rows = []

# Group by 'Contract Name' and process each group
for contract_name, group in df.groupby('Contract Name'):
    if len(group) < 2:
        continue

    # Get the latest row and the next (previous) row
    latest_row = group.iloc[0]
    next_row = group.iloc[1]

    # Calculate net % change using the provided formula
    net_percentage_change = calculate_net_percentage_change(
        current_long=latest_row['Noncommercial Long'],
        current_short=latest_row['Noncommercial Short'],
        previous_long=next_row['Noncommercial Long'],
        previous_short=next_row['Noncommercial Short']
    )

    # Make short positions positive (absolute values)
    latest_row['Noncommercial Short'] = abs(latest_row['Noncommercial Short'])
    latest_row['Noncommercial Short, Change'] = abs(latest_row['Noncommercial Short, Change'])

    # Calculate total (Long + Short)
    total = latest_row['Noncommercial Long'] + latest_row['Noncommercial Short']

    # Calculate Long % and Short %
    long_percentage = (latest_row['Noncommercial Long'] / total) * 100
    short_percentage = (latest_row['Noncommercial Short'] / total) * 100

    # Add the calculated values to the latest row
    latest_row['Net % Change'] = net_percentage_change
    latest_row['Long %'] = round(long_percentage, 2)
    latest_row['Short %'] = round(short_percentage, 2)

    # Append the row to the final rows list
    final_rows.append(latest_row)

# Create the final DataFrame from the processed rows
df_cleaned = pd.DataFrame(final_rows)

# Rename the columns as required
df_cleaned = df_cleaned.rename(columns={
    'Contract Name': 'Asset',
    'Noncommercial Long': 'Long',
    'Noncommercial Short': 'Short',
    'Noncommercial Long, Change': 'Delta Long',
    'Noncommercial Short, Change': 'Delta Short',
    'Net Position, Large Spec': 'Net Position',
    'Open Interest': 'Open Interest',
    'Open Interest, Change': 'Open Interest Change'
})

# Reorder the columns
df_cleaned = df_cleaned[['Asset', 'Long', 'Short', 'Delta Long', 'Delta Short', 'Long %', 'Short %', 'Net % Change', 
                         'Net Position', 'Open Interest', 'Open Interest Change', 'Date']]

# Save the cleaned data to a new CSV file
df_cleaned.to_csv('cot_data_cleaned.csv', index=False)

print("Cleaned Data:")
print(df_cleaned.head())
