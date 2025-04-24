import pandas as pd
import numpy as np
from pathlib import Path
import glob

class HealthProfileClassifier:
    def __init__(self):
        self.persona_thresholds = {
            'health_conscious': {
                'daily_steps_min': 7000,
                'exercise_minutes_daily': 30,
                'mindfulness_minutes_daily': 15,
                'sleep_duration_min': 7.0,
                'deep_sleep_min': 20,
                'rem_sleep_min': 25
            },
            'mild_anxiety': {
                'hr_afternoon_max': 85,
                'hrv_min': 30,
                'mindfulness_minutes_daily': 0,
                'missed_lunch_threshold': 200  # steps during lunch hours
            },
            'academic_stress': {
                'rem_sleep_max': 15,
                'late_night_activity': True,
                'sleep_duration_min': 5.0,
                'study_period_hr_max': 85
            },
            'sleep_issues': {
                'daily_steps_max': 3500,
                'exercise_minutes_daily': 10,
                'sleep_duration_max': 6.0,
                'deep_sleep_max': 15,
                'sleep_interruptions': True
            },
            'burnout': {
                'resting_hr_min': 75,
                'hrv_max': 40,
                'mindfulness_weekday': 0,
                'work_hours_activity': True,
                'headphone_exposure_min': 65
            },
            'night_shift': {
                'night_steps_min': 8000,
                'day_steps_max': 2000,
                'sleep_duration_max': 5.0,
                'night_activity': True,
                'day_sleep': True
            }
        }

    def _calculate_daily_patterns(self, data):
        """Calculate daily health patterns from hourly data."""
        # Convert Date and Time columns to datetime index
        data['datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        
        patterns = {}
        
        # Daily averages
        patterns['daily_steps'] = data.groupby(data['datetime'].dt.date)['Step Count (steps)'].sum().mean()
        patterns['daily_exercise'] = data.groupby(data['datetime'].dt.date)['Exercise Minutes (minutes)'].sum().mean()
        patterns['daily_mindfulness'] = data.groupby(data['datetime'].dt.date)['Mindfulness Minutes (minutes)'].sum().mean()
        
        # Sleep patterns
        sleep_data = data[data['Sleep Duration (hours)'] > 0]
        patterns['avg_sleep_duration'] = sleep_data['Sleep Duration (hours)'].mean() if not sleep_data.empty else 0
        patterns['avg_deep_sleep'] = sleep_data['Deep Sleep (%)'].mean() if not sleep_data.empty else 0
        patterns['avg_rem_sleep'] = sleep_data['REM Sleep (%)'].mean() if not sleep_data.empty else 0
        
        # Get most common sleep start hour
        if not sleep_data.empty:
            sleep_hours = sleep_data['datetime'].dt.hour.value_counts()
            patterns['sleep_start_hour'] = sleep_hours.index[0] if not sleep_hours.empty else 0
        else:
            patterns['sleep_start_hour'] = 0
            
        patterns['sleep_interruptions'] = (sleep_data['Time Awake (minutes)'] > 30).any() if not sleep_data.empty else False
        
        # Time-based patterns
        day_mask = data['datetime'].dt.hour.between(9, 17, inclusive='both')
        night_mask = ~data['datetime'].dt.hour.between(7, 21, inclusive='both')
        lunch_mask = data['datetime'].dt.hour.between(12, 13, inclusive='both')
        
        patterns['day_steps'] = data[day_mask]['Step Count (steps)'].mean()
        patterns['night_steps'] = data[night_mask]['Step Count (steps)'].mean()
        patterns['lunch_steps'] = data[lunch_mask]['Step Count (steps)'].mean()
        
        # Stress indicators
        patterns['avg_day_hr'] = data[day_mask]['Heart Rate (bpm)'].mean()
        patterns['avg_hrv'] = data['Heart Rate Variability (ms)'].mean()
        patterns['headphone_exposure'] = data['Headphone Audio Exposure (dB)'].mean()
        
        # Activity timing
        patterns['night_activity'] = data[night_mask]['Step Count (steps)'].mean() > 500
        
        # Check for day sleep (sleep periods during day hours)
        if not sleep_data.empty:
            patterns['day_sleep'] = sleep_data['datetime'].dt.hour.between(9, 17, inclusive='both').any()
        else:
            patterns['day_sleep'] = False
        
        return patterns

    def _score_persona(self, patterns, persona):
        """Calculate match score for a specific persona."""
        thresholds = self.persona_thresholds[persona]
        score = 0
        max_score = 100
        
        if persona == 'health_conscious':
            if patterns['daily_steps'] >= thresholds['daily_steps_min']:
                score += 25
            if patterns['daily_exercise'] >= thresholds['exercise_minutes_daily']:
                score += 25
            if patterns['daily_mindfulness'] >= thresholds['mindfulness_minutes_daily']:
                score += 25
            if (patterns['avg_sleep_duration'] >= thresholds['sleep_duration_min'] and
                patterns['avg_deep_sleep'] >= thresholds['deep_sleep_min'] and
                patterns['avg_rem_sleep'] >= thresholds['rem_sleep_min']):
                score += 25
                
        elif persona == 'mild_anxiety':
            if patterns['avg_day_hr'] > thresholds['hr_afternoon_max']:
                score += 30
            if patterns['avg_hrv'] < thresholds['hrv_min']:
                score += 30
            if patterns['daily_mindfulness'] <= thresholds['mindfulness_minutes_daily']:
                score += 20
            if patterns['lunch_steps'] < thresholds['missed_lunch_threshold']:
                score += 20
                
        elif persona == 'academic_stress':
            if patterns['avg_rem_sleep'] < thresholds['rem_sleep_max']:
                score += 35
            if patterns['night_activity']:
                score += 35
            if patterns['avg_sleep_duration'] < thresholds['sleep_duration_min']:
                score += 30
                
        elif persona == 'sleep_issues':
            if patterns['daily_steps'] <= thresholds['daily_steps_max']:
                score += 25
            if patterns['daily_exercise'] <= thresholds['exercise_minutes_daily']:
                score += 25
            if (patterns['avg_sleep_duration'] <= thresholds['sleep_duration_max'] and
                patterns['avg_deep_sleep'] <= thresholds['deep_sleep_max']):
                score += 25
            if patterns['sleep_interruptions']:
                score += 25
                
        elif persona == 'burnout':
            if patterns['avg_day_hr'] >= thresholds['resting_hr_min']:
                score += 25
            if patterns['avg_hrv'] <= thresholds['hrv_max']:
                score += 25
            if patterns['daily_mindfulness'] <= thresholds['mindfulness_weekday']:
                score += 25
            if patterns['headphone_exposure'] >= thresholds['headphone_exposure_min']:
                score += 25
                
        elif persona == 'night_shift':
            if patterns['night_steps'] >= thresholds['night_steps_min']:
                score += 25
            if patterns['day_steps'] <= thresholds['day_steps_max']:
                score += 25
            if patterns['avg_sleep_duration'] <= thresholds['sleep_duration_max']:
                score += 25
            if patterns['day_sleep']:
                score += 25
                
        return (score / max_score) * 100

    def classify_profile(self, data):
        """Classify a health profile into one of the personas."""
        daily_patterns = self._calculate_daily_patterns(data)
        
        scores = {}
        for persona in self.persona_thresholds.keys():
            scores[persona] = self._score_persona(daily_patterns, persona)
            
        # Debug output
        print("\nScores for each persona:")
        for persona, score in scores.items():
            print(f"{persona}: {score:.2f}%")
        print("\nDaily Patterns:")
        for key, value in daily_patterns.items():
            print(f"{key}: {value}")
            
        best_match = max(scores.items(), key=lambda x: x[1])
        return best_match[0], best_match[1]

    def process_profiles(self):
        """Process all profiles in the profiles directory."""
        profiles_dir = Path("./profiles")
        if not profiles_dir.exists():
            print(f"Profiles directory not found at: {profiles_dir.absolute()}")
            return
        
        results = []
        profile_files = glob.glob(str(profiles_dir / "*.csv"))
        
        print(f"Found {len(profile_files)} profile(s) to process")
        print("Profile files:", profile_files)
        
        for file_path in profile_files:
            try:
                print(f"\nProcessing: {file_path}")
                data = pd.read_csv(file_path)
                profile_id = Path(file_path).stem
                persona, confidence = self.classify_profile(data)
                
                results.append({
                    'Profile_ID': profile_id,
                    'Matched_Persona': persona,
                    'Confidence_Score': confidence
                })
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
        
        if results:
            results_df = pd.DataFrame(results)
            results_df.to_csv('classification_results.csv', index=False)
            print("\nResults saved to classification_results.csv")
            print("\nClassification Summary:")
            print(results_df)
        else:
            print("No results to save")

if __name__ == "__main__":
    classifier = HealthProfileClassifier()
    classifier.process_profiles()