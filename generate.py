import os
import random
import pandas as pd
from datetime import datetime
import argparse

# Path to the health data directory
HEALTH_DATA_DIR = "./LBG Reboot 2025 LDN - Health Demo Data"
# Path to save the new profiles
PROFILES_DIR = "./profiles"

# Create profiles directory if it doesn't exist
os.makedirs(PROFILES_DIR, exist_ok=True)

def get_random_csv():
    """Randomly select one of the CSV files from the health data directory."""
    csv_files = [f for f in os.listdir(HEALTH_DATA_DIR) if f.endswith('.csv')]
    return os.path.join(HEALTH_DATA_DIR, random.choice(csv_files))

def apply_random_variation(value, percentage=10):
    """Apply a random variation of ±percentage% to the given value."""
    if pd.isna(value) or value == 0:
        return value
    
    variation = random.uniform(-percentage/100, percentage/100)
    return value * (1 + variation)

def generate_new_health_data():
    """Generate new health data by modifying an existing CSV file."""
    # Get a random CSV file
    csv_file = get_random_csv()
    print(f"Selected file: {csv_file}")
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Store original column types
    original_dtypes = df.dtypes.to_dict()
    
    # Get numeric columns (excluding Date and Time)
    numeric_columns = [col for col in df.columns if col not in ['Date', 'Time'] 
                      and df[col].dtype in [float, int]]
    
    # Apply random variation to each numeric column
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: apply_random_variation(x))
    
    # Convert back to original data types
    for col, dtype in original_dtypes.items():
        if col in numeric_columns:
            if pd.api.types.is_integer_dtype(dtype):
                df[col] = df[col].round().astype(dtype)
    
    # Get the next ID counter
    existing_files = [f for f in os.listdir(PROFILES_DIR) if f.endswith('.csv')]
    counter = len(existing_files) + 1
    
    # Generate a new filename
    new_filename = f"{counter}.csv"
    output_path = os.path.join(PROFILES_DIR, new_filename)
    
    # Save the modified data
    df.to_csv(output_path, index=False)
    print(f"Generated new health data: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Add argument parser
    parser = argparse.ArgumentParser(description='Generate health data profiles')
    parser.add_argument('--num-profiles', type=int, default=30,
                      help='Number of profiles to generate (default: 30)')
    
    args = parser.parse_args()
    
    # Generate the specified number of health data profiles
    for i in range(args.num_profiles):
        new_file = generate_new_health_data()
        print(f"Generated profile {i+1} of {args.num_profiles}")
    print(f"All {args.num_profiles} profiles have been generated!")