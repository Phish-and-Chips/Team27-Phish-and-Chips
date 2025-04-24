#!/usr/bin/env python3
"""
Generate health data for multiple profiles
This script generates health data for 25 different profiles.

Usage:
    python generate_all_profiles.py --start-date <YYYY-MM-DD> --days <number_of_days>
    
Example:
    python generate_all_profiles.py --start-date 2025-03-01 --days 30
"""

import os
import argparse
from generate_health_data import HealthDataGenerator

def parse_args():
    parser = argparse.ArgumentParser(description="Generate health data for multiple profiles")
    parser.add_argument("--start-date", type=str, default="2025-03-01",
                      help="Start date in YYYY-MM-DD format (default: 2025-03-01)")
    parser.add_argument("--days", type=int, default=30,
                      help="Number of days to generate (default: 30)")
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        
        # Create profiles directory if it doesn't exist
        os.makedirs("profiles", exist_ok=True)
        
        # Generate 25 profiles
        for i in range(1, 26):
            profile_num = i + 6  # Start from 7
            output_file = f"profiles/{profile_num}_health_data.csv"
            description = f"Health Profile {profile_num}"
            
            print(f"Generating data for {description}...")
            generator = HealthDataGenerator(profile_type="generic")  # Using generic profile type
            df = generator.generate_days(args.start_date, args.days)
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            print(f"Data saved to: {output_file}")
        
        print("\nAll profiles generated successfully!")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        exit(1)

if __name__ == "__main__":
    main() 