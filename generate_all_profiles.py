#!/usr/bin/env python3
"""
Generate health data for multiple profiles
This script generates health data for 25 different profiles with random variations.

Usage:
    python generate_all_profiles.py --start-date <YYYY-MM-DD> --days <number_of_days>
    
Example:
    python generate_all_profiles.py --start-date 2025-03-01 --days 30
"""

import os
import argparse
import random
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
        
        # Available base profiles
        base_profiles = [
            "liwei_control",
            "samira_anxiety",
            "javier_student",
            "aisha_sleep",
            "kofi_burnout",
            "ahmed_nightshift"
        ]
        
        # Generate 25 profiles
        for i in range(1, 26):
            profile_num = i + 6  # Start from 7
            # Randomly select a base profile
            base_profile = random.choice(base_profiles)
            output_file = f"profiles/{profile_num}_{base_profile}_health_data.csv"
            description = f"Health Profile {profile_num} (based on {base_profile})"
            
            print(f"Generating data for {description} (based on {base_profile})...")
            generator = HealthDataGenerator(profile_type=base_profile)
            
            # Add random variations to the profile
            generator.add_variations(
                sleep_time_variation=random.randint(-2, 2),  # Vary sleep time by ±2 hours
                training_time_variation=random.randint(-3, 3),  # Vary training time by ±3 hours
                skip_training_probability=random.uniform(0, 0.3),  # 0-30% chance to skip training
                poor_sleep_probability=random.uniform(0, 0.4),  # 0-40% chance of poor sleep
                mindfulness_variation=random.uniform(0.5, 1.5)  # Vary mindfulness by 50-150%
            )
            
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