import pandas as pd

def filter_and_save_csv(input_csv, output_csv):
    # Read the input CSV file
    df = pd.read_csv(input_csv)
    
    # Convert the 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Filter rows to include only July 15th dates
    df = df[df['Time'].dt.month == 7]
    df = df[df['Time'].dt.day == 15]
    
    # Extract only the year from the 'Time' column
    df['Time'] = df['Time'].dt.year
    
    # Drop the 'GMSL' column
    df = df.drop(columns=['GMSL uncertainty'])
    
    # Save the filtered data to a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage: Filter the sea_level_data.csv and save the result to output.csv
filter_and_save_csv("sea_level_data.csv", "output.csv")
