"""
This script processes a COT (Commitment of Traders) data CSV file using an object-oriented approach:
1. A COTData class is created for each row of data.
2. Each contract row (i.e., each asset) has attributes like 'Long', 'Short', 'Delta Long', etc.
3. Methods handle the calculation of percentages and net changes.
4. The script processes the CSV and outputs the cleaned file.
"""

import pandas as pd

class COTData:
    def __init__(self, contract_name, long, short, delta_long, delta_short, net_position, open_interest, open_interest_change, date):
        self.contract_name = contract_name
        self.long = long
        self.short = abs(short)  # Ensure short is positive
        self.delta_long = delta_long
        self.delta_short = abs(delta_short)  # Ensure delta short is positive
        self.net_position = net_position
        self.open_interest = open_interest
        self.open_interest_change = open_interest_change
        self.date = date
        self.long_percentage = 0.0
        self.short_percentage = 0.0
        self.net_percentage_change = 0.0

    def calculate_percentages(self):
        total = self.long + self.short
        if total != 0:
            self.long_percentage = (self.long / total) * 100
            self.short_percentage = (self.short / total) * 100

    def calculate_net_percentage_change(self, previous_long, previous_short):
        previous_short = abs(previous_short)  # Make sure the previous short is positive
        if previous_long + previous_short != 0:
            current_long_percentage = self.long / (self.long + self.short)
            previous_long_percentage = previous_long / (previous_long + previous_short)
            self.net_percentage_change = round((current_long_percentage - previous_long_percentage) * 100, 2)

    def to_dict(self):
        return {
            'Asset': self.contract_name,
            'Long': self.long,
            'Short': self.short,
            'Delta Long': self.delta_long,
            'Delta Short': self.delta_short,
            'Long %': round(self.long_percentage, 2),
            'Short %': round(self.short_percentage, 2),
            'Net % Change': self.net_percentage_change,
            'Net Position': self.net_position,
            'Open Interest': self.open_interest,
            'Open Interest Change': self.open_interest_change,
            'Date': self.date
        }


def process_cot_data(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter the DataFrame to only include rows from the current year (2024)
    df = df[df['Date'].dt.year == 2024]

    # Sort the DataFrame by 'Contract Name' and 'Date' in descending order
    df = df.sort_values(by=['Contract Name', 'Date'], ascending=[True, False])

    # Initialize an empty list to store final COTData objects
    cot_data_objects = []

    # Group by 'Contract Name' and process each group
    for contract_name, group in df.groupby('Contract Name'):
        if len(group) < 2:
            continue

        # Get the latest row and the next (previous) row
        latest_row = group.iloc[0]
        next_row = group.iloc[1]

        # Create COTData object for the latest row
        cot_data = COTData(
            contract_name=latest_row['Contract Name'],
            long=latest_row['Noncommercial Long'],
            short=latest_row['Noncommercial Short'],
            delta_long=latest_row['Noncommercial Long, Change'],
            delta_short=latest_row['Noncommercial Short, Change'],
            net_position=latest_row['Net Position, Large Spec'],
            open_interest=latest_row['Open Interest'],
            open_interest_change=latest_row['Open Interest, Change'],
            date=latest_row['Date']
        )

        # Calculate the Long% and Short% for the current row
        cot_data.calculate_percentages()

        # Calculate the Net% Change compared to the previous row
        cot_data.calculate_net_percentage_change(
            previous_long=next_row['Noncommercial Long'],
            previous_short=next_row['Noncommercial Short']
        )

        # Append the COTData object to the list
        cot_data_objects.append(cot_data)

    # Convert the list of COTData objects to a list of dictionaries
    cleaned_data = [cot.to_dict() for cot in cot_data_objects]

    # Create a DataFrame from the cleaned data
    df_cleaned = pd.DataFrame(cleaned_data)

    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv('cot_data_cleaned.csv', index=False)

    return df_cleaned


# Process the COT data
df_cleaned = process_cot_data('cot-reports.csv')


