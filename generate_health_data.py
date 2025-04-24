#!/usr/bin/env python3
"""
Health Data Generator
Generates synthetic health monitoring data for different user profiles

Usage:
    python generate_health_data.py --profile <profile_type> --output <output_file> --start-date <YYYY-MM-DD>
    
Example:
    python generate_health_data.py --profile liwei_control --output data/1_liwei_control_health_conscious_young_adult.csv --start-date 2025-03-01
"""

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error: Required package missing - {e}")
    print("Please install required packages using:")
    print("pip install pandas numpy")
    exit(1)

from datetime import datetime, timedelta
import random
import os
import argparse

class HealthDataGenerator:
    def __init__(self, profile_type="generic"):
        self.profile_type = profile_type
        self.profile_configs = {
            # Generic profile for numbered profiles
            "generic": {
                "resting_hr": (60, 75),  # (min, max)
                "active_hr": (120, 150),
                "resting_hrv": (40, 60),
                "active_hrv": (25, 35),
                "vo2_max": (35, 45),
                "sleep_duration": (6.5, 8.0),
                "training_times": [(7, 8), (18, 19)],  # (start_hour, end_hour)
                "training_pace": (5.5, 6.5),
                "mindfulness_minutes": (5, 15),
                "daily_steps": (5000, 8000),
                "deep_sleep": (15, 25),
                "rem_sleep": (20, 25)
            },
            # 1. Li Wei - Health-Conscious Young Adult
            "liwei_control": {
                "resting_hr": (55, 65),  # (min, max)
                "active_hr": (120, 140),
                "resting_hrv": (70, 85),
                "active_hrv": (40, 55),
                "vo2_max": (45, 52),
                "sleep_duration": (7.5, 8.0),
                "training_times": [(6, 7), (18, 19)],  # (start_hour, end_hour)
                "training_pace": (5.0, 6.0),
                "mindfulness_minutes": (15, 20),
                "daily_steps": (7000, 8000),
                "deep_sleep": (18, 22),
                "rem_sleep": (23, 27)
            },
            # 2. Samira - Young Adult with Mild Anxiety
            "samira_anxiety": {
                "resting_hr": (70, 85),
                "active_hr": (140, 160),
                "resting_hrv": (25, 45),
                "active_hrv": (15, 25),
                "vo2_max": (35, 42),
                "sleep_duration": (6, 7),
                "training_times": [(18, 19)],
                "training_pace": (6.0, 7.0),
                "mindfulness_minutes": (0, 5),  # Plans but rarely follows through
                "daily_steps": (5000, 6500),
                "deep_sleep": (10, 15),
                "rem_sleep": (15, 20)
            },
            # 3. Javier - Gen Z Student under Academic & Financial Stress
            "javier_student": {
                "resting_hr": (65, 75),
                "active_hr": (130, 150),
                "resting_hrv": (30, 50),
                "active_hrv": (20, 30),
                "vo2_max": (38, 45),
                "sleep_duration": (5, 6.5),
                "training_times": [(20, 21)],  # Evening after work
                "training_pace": (6.5, 7.5),
                "mindfulness_minutes": (5, 10),
                "daily_steps": (6000, 7500),
                "deep_sleep": (12, 18),
                "rem_sleep": (12, 18)  # Below 15% during term-end
            },
            # 4. Aisha - Young Adult with Sleep Issues & Low Activity
            "aisha_sleep": {
                "resting_hr": (60, 70),
                "active_hr": (125, 145),
                "resting_hrv": (35, 55),
                "active_hrv": (25, 35),
                "vo2_max": (32, 40),
                "sleep_duration": (4, 6),  # 4-6 hours of broken sleep
                "training_times": [(10, 11)],  # Mid-morning
                "training_pace": (7.0, 8.0),
                "mindfulness_minutes": (0, 5),
                "daily_steps": (2500, 3500),  # 3000/day
                "deep_sleep": (8, 12),  # Just 10% deep rest
                "rem_sleep": (15, 20)
            },
            # 5. Kofi - Young Professional Experiencing Burnout
            "kofi_burnout": {
                "resting_hr": (75, 90),  # Driven upward
                "active_hr": (145, 165),
                "resting_hrv": (20, 35),  # Driven downward
                "active_hrv": (10, 20),
                "vo2_max": (40, 48),
                "sleep_duration": (6.5, 7.5),
                "training_times": [(7, 8)],  # Morning before work
                "training_pace": (5.5, 6.5),
                "mindfulness_minutes": (0, 5),  # Drops to zero on weekdays
                "daily_steps": (5500, 7000),
                "deep_sleep": (15, 20),
                "rem_sleep": (20, 25)
            },
            # 6. Ahmed - Night-Shift Worker with Circadian Disruption
            "ahmed_nightshift": {
                "resting_hr": (60, 75),
                "active_hr": (130, 150),
                "resting_hrv": (30, 50),
                "active_hrv": (20, 30),
                "vo2_max": (35, 42),
                "sleep_duration": (4, 5),  # 4 hours on shift nights, 4.9 on rest days
                "training_times": [(14, 15)],  # Afternoon after night shift
                "training_pace": (6.0, 7.0),
                "mindfulness_minutes": (5, 10),
                "daily_steps": (7000, 9000),  # 8600 steps per shift night
                "deep_sleep": (10, 15),
                "rem_sleep": (15, 20)
            }
        }
        
        if profile_type not in self.profile_configs:
            raise ValueError(f"Unknown profile type: {profile_type}. Available profiles: {list(self.profile_configs.keys())}")

    def generate_hourly_data(self, date, hour):
        try:
            config = self.profile_configs[self.profile_type]
            is_training_hour = any(start <= hour < end for start, end in config["training_times"])
            is_sleep_hour = 22 <= hour or hour <= 4
            
            # Base metrics
            if is_training_hour:
                heart_rate = random.uniform(*config["active_hr"])
                hrv = random.uniform(*config["active_hrv"])
                steps = random.randint(2000, 2800)
                distance = random.uniform(5.0, 6.0)
                calories = random.randint(550, 650)
                exercise_mins = random.randint(45, 60)
                pace = random.uniform(*config["training_pace"])
            elif is_sleep_hour:
                heart_rate = random.uniform(*config["resting_hr"])
                hrv = random.uniform(*config["resting_hrv"])
                steps = 0
                distance = 0
                calories = 62
                exercise_mins = 0
                pace = 0
            else:
                heart_rate = random.uniform(50, 65)
                hrv = random.uniform(75, 85)
                steps = random.randint(400, 800)
                distance = random.uniform(0.3, 0.8)
                calories = random.randint(80, 120)
                exercise_mins = 0
                pace = 0
            
            # Sleep metrics
            if is_sleep_hour:
                sleep_duration = config["sleep_duration"][0] if hour == 2 else 0
                sleep_rem = random.randint(*config["rem_sleep"]) if hour == 2 else 0
                sleep_core = 100 - sleep_rem - random.randint(*config["deep_sleep"]) if hour == 2 else 0
                sleep_deep = random.randint(*config["deep_sleep"]) if hour == 2 else 0
            else:
                sleep_duration = sleep_rem = sleep_core = sleep_deep = 0
                
            # Mindfulness
            mindfulness = random.randint(*config["mindfulness_minutes"]) if hour in [7, 17, 20] else 0
            
            return {
                "Date": date.strftime("%d-%b-%Y"),
                "Time": f"{hour:02d}:00:00",
                "Heart Rate (bpm)": round(heart_rate, 1),
                "Heart Rate Variability (ms)": round(hrv, 1),
                "Respiratory Rate (breaths/min)": round(random.uniform(11, 22) if is_training_hour else random.uniform(11, 14), 1),
                "Blood Oxygen (%)": round(random.uniform(97.5, 99.5), 1),
                "Step Count (steps)": steps,
                "Walking Speed (km/h)": round(random.uniform(12, 14) if is_training_hour else random.uniform(3, 5), 1),
                "Distance Walked/Run (km)": round(distance, 1),
                "Flights Climbed (flights)": random.randint(0, 5),
                "Active Energy Burned (kcal)": calories,
                "Stand Hours (hours)": 0 if is_sleep_hour else 1,
                "Sleep Duration (hours)": sleep_duration,
                "Time Awake (minutes)": random.randint(5, 15) if is_sleep_hour else 0,
                "REM Sleep (%)": sleep_rem,
                "Core Sleep (%)": sleep_core,
                "Deep Sleep (%)": sleep_deep,
                "Environmental Sound Level (dB)": round(random.uniform(30, 50), 1),
                "Headphone Audio Exposure (dB)": round(random.uniform(65, 75), 1) if is_training_hour else 0,
                "VO2 Max (mL/kg/min)": round(random.uniform(*config["vo2_max"]), 1),
                "ECG (ST Segment Elevation) (mm)": round(random.uniform(-0.05, 0.05), 3),
                "Body Temperature (°C)": round(random.uniform(36.2, 36.5) + (0.7 if is_training_hour else 0), 2),
                "Exercise Minutes (minutes)": exercise_mins,
                "Elevation Gain (meters)": random.randint(0, 35) if is_training_hour else random.randint(0, 5),
                "Running Pace (min/km)": round(pace, 1),
                "Mindfulness Minutes (minutes)": mindfulness
            }
        except Exception as e:
            print(f"Error generating hourly data: {e}")
            raise

    def generate_days(self, start_date, num_days=30):
        try:
            data = []
            current_date = datetime.strptime(start_date, "%Y-%m-%d")
            
            for day in range(num_days):
                for hour in range(24):
                    data.append(self.generate_hourly_data(current_date, hour))
                current_date += timedelta(days=1)
                
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error generating days: {e}")
            raise

def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic health monitoring data for different user profiles")
    parser.add_argument("--profile", type=str, required=True,
                      help="Profile type (e.g., generic, liwei_control, samira_anxiety, javier_student, aisha_sleep, kofi_burnout, ahmed_nightshift)")
    parser.add_argument("--output", type=str, required=True,
                      help="Output CSV file path")
    parser.add_argument("--start-date", type=str, default="2025-03-01",
                      help="Start date in YYYY-MM-DD format (default: 2025-03-01)")
    parser.add_argument("--days", type=int, default=30,
                      help="Number of days to generate (default: 30)")
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        
        # Generate data
        generator = HealthDataGenerator(profile_type=args.profile)
        df = generator.generate_days(args.start_date, args.days)
        
        # Save to CSV
        df.to_csv(args.output, index=False)
        print(f"Successfully generated health data for profile: {args.profile}")
        print(f"Data saved to: {args.output}")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        exit(1)

if __name__ == "__main__":
    main() 