
# Personalized Health Monitoring Agent

# This script loads and analyzes health data for a specific persona.


import pandas as pd
import os

# Define thresholds (these can be refined based on clinical guidelines or further analysis)
HIGH_HR_THRESHOLD = 90  # Example threshold for elevated heart rate (bpm)
LOW_HRV_THRESHOLD = 40   # Example threshold for low heart rate variability (ms)
LOW_DEEP_SLEEP_THRESHOLD = 15 # Example threshold for low deep sleep percentage
LOW_REM_SLEEP_THRESHOLD = 15   # Example threshold for low REM sleep percentage
EXPECTED_MINDFULNESS_MINUTES = 10 # Based on Samira's description
ANXIETY_SPIKE_HOUR_START = 14 # Afternoon panic mentioned around deadlines (2 PM)
ANXIETY_SPIKE_HOUR_END = 17   # (5 PM)

def load_health_data(file_path: str) -> pd.DataFrame | None:
    """Loads health data from a CSV file."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    try:
        df = pd.read_csv(file_path)
        # Convert Date and Time to a single datetime column
        df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d-%b-%Y %H:%M:%S')
        df.set_index('Timestamp', inplace=True)
        print(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

def analyze_samira_data(df: pd.DataFrame):
    """Analyzes health data specifically for Samira's persona."""
    print("\n--- Analyzing Samira's Data (Young Adult with Mild Anxiety) ---")

    # 1. Check for potential afternoon anxiety spikes
    afternoon_data = df.between_time(f'{ANXIETY_SPIKE_HOUR_START}:00', f'{ANXIETY_SPIKE_HOUR_END}:00')
    potential_spikes = afternoon_data[
        (afternoon_data['Heart Rate (bpm)'] > HIGH_HR_THRESHOLD) |
        (afternoon_data['Heart Rate Variability (ms)'] < LOW_HRV_THRESHOLD)
    ]
    if not potential_spikes.empty:
        print(f"\nPotential Anxiety Indicators Detected ({len(potential_spikes)} instances between {ANXIETY_SPIKE_HOUR_START}:00 and {ANXIETY_SPIKE_HOUR_END}:00):")
        print(potential_spikes[['Heart Rate (bpm)', 'Heart Rate Variability (ms)']].head())
    else:
        print(f"\nNo significant anxiety indicators detected during the afternoon ({ANXIETY_SPIKE_HOUR_START}:00 - {ANXIETY_SPIKE_HOUR_END}:00).")

    # 2. Check mindfulness adherence (around 21:00)
    mindfulness_time_data = df[df.index.hour == 21]
    missed_sessions = mindfulness_time_data[mindfulness_time_data['Mindfulness Minutes (minutes)'] == 0]
    total_planned_sessions = len(mindfulness_time_data)
    if total_planned_sessions > 0:
        missed_percentage = (len(missed_sessions) / total_planned_sessions) * 100
        print(f"\nMindfulness Adherence (around 21:00):")
        print(f"- Planned sessions checked: {total_planned_sessions}")
        print(f"- Missed sessions (0 minutes logged): {len(missed_sessions)} ({missed_percentage:.1f}%)")
    else:
        print("\nNo mindfulness data found around 21:00.")

    # 3. Analyze Sleep Quality (Data is usually logged once per day, often in the morning)
    # Find rows where sleep duration is logged (likely indicating end of sleep block)
    sleep_summary_data = df[df['Sleep Duration (hours)'] > 0].copy()
    if not sleep_summary_data.empty:
        sleep_summary_data['Poor Deep Sleep'] = sleep_summary_data['Deep Sleep (%)'] < LOW_DEEP_SLEEP_THRESHOLD
        sleep_summary_data['Poor REM Sleep'] = sleep_summary_data['REM Sleep (%)'] < LOW_REM_SLEEP_THRESHOLD

        avg_deep_sleep = sleep_summary_data['Deep Sleep (%)'].mean()
        avg_rem_sleep = sleep_summary_data['REM Sleep (%)'].mean()
        poor_deep_sleep_days = sleep_summary_data['Poor Deep Sleep'].sum()
        poor_rem_sleep_days = sleep_summary_data['Poor REM Sleep'].sum()

        print("\nSleep Quality Analysis:")
        print(f"- Average Deep Sleep: {avg_deep_sleep:.1f}% (Threshold: < {LOW_DEEP_SLEEP_THRESHOLD}%)")
        print(f"- Average REM Sleep: {avg_rem_sleep:.1f}% (Threshold: < {LOW_REM_SLEEP_THRESHOLD}%)")
        print(f"- Days with potentially low Deep Sleep: {poor_deep_sleep_days} / {len(sleep_summary_data)}")
        print(f"- Days with potentially low REM Sleep: {poor_rem_sleep_days} / {len(sleep_summary_data)}")
    else:
        print("\nNo sleep summary data found.")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    # Determine the base path relative to the script location or workspace root
    # This assumes the script is run from the workspace root or its path is relative to it
    base_data_path = "Team27-Phish-and-Chips/LBG Reboot 2025 LDN - Health Demo Data"
    samira_file = "2_samira_young_adult_mild_anxiety.csv"
    file_path = os.path.join(base_data_path, samira_file)

    health_df = load_health_data(file_path)

    if health_df is not None:
        analyze_samira_data(health_df) 