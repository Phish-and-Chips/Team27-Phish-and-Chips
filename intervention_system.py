"""
Adaptive Intervention System

This component generates personalized interventions based on health data analysis.
It works in conjunction with the health_monitor.py to deliver appropriate
recommendations at the right time.
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any

# Import from health_monitor to reuse functions
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from health_monitor import load_health_data

# Intervention types
class InterventionType:
    BREATHING = "breathing_exercise"
    MINDFULNESS = "mindfulness_session"
    PHYSICAL = "physical_activity"
    SLEEP = "sleep_improvement"
    WORK_BREAK = "work_break"
    HYDRATION = "hydration_reminder"
    STRESS_MANAGEMENT = "stress_management"


class AdaptiveInterventionSystem:
    def __init__(self, health_data: pd.DataFrame, persona_type: str):
        """
        Initialize the intervention system with health data and persona type.
        
        Args:
            health_data: DataFrame containing health metrics
            persona_type: String identifier for persona (e.g., "samira", "kofi")
        """
        self.health_data = health_data
        self.persona_type = persona_type.lower()
        self.intervention_history = []
        
        # Initialize persona-specific settings
        self._initialize_persona_settings()
        
    def _initialize_persona_settings(self):
        """Set up persona-specific parameters and thresholds."""
        self.settings = {
            "samira": {
                "priority_interventions": [
                    InterventionType.BREATHING,
                    InterventionType.WORK_BREAK,
                    InterventionType.STRESS_MANAGEMENT
                ],
                "optimal_intervention_times": {
                    # Morning break
                    "morning": [(10, 30), (11, 30)],
                    # Afternoon anxiety spike period
                    "afternoon": [(14, 0), (17, 0)],
                    # Evening mindfulness reminder
                    "evening": [(20, 45), (21, 15)]
                },
                "max_daily_interventions": 5
            },
            "kofi": {
                "priority_interventions": [
                    InterventionType.MINDFULNESS,
                    InterventionType.WORK_BREAK,
                    InterventionType.STRESS_MANAGEMENT
                ],
                "optimal_intervention_times": {
                    "morning": [(9, 30), (10, 30)],
                    "afternoon": [(13, 0), (15, 0)],
                    "evening": [(18, 30), (19, 30)]
                },
                "max_daily_interventions": 4
            },
            # Add other personas as needed
            "default": {
                "priority_interventions": [
                    InterventionType.BREATHING,
                    InterventionType.MINDFULNESS,
                    InterventionType.PHYSICAL
                ],
                "optimal_intervention_times": {
                    "morning": [(9, 0), (11, 0)],
                    "afternoon": [(14, 0), (16, 0)],
                    "evening": [(19, 0), (21, 0)]
                },
                "max_daily_interventions": 3
            }
        }
        
        # Use default if persona not found
        if self.persona_type not in self.settings:
            print(f"Persona '{self.persona_type}' not found. Using default settings.")
            self.persona_type = "default"
            
    def analyze_and_recommend(self, current_datetime: datetime = None) -> Dict[str, Any]:
        """
        Analyze health data and return recommended intervention.
        
        Args:
            current_datetime: The current date and time (defaults to now)
            
        Returns:
            Dictionary containing intervention details
        """
        if current_datetime is None:
            current_datetime = datetime.now()
            
        # Get relevant recent data (last 24 hours)
        recent_data = self._get_recent_data(current_datetime)
        
        # Detect conditions
        conditions = self._detect_conditions(recent_data, current_datetime)
        
        # Get appropriate time period (morning, afternoon, evening)
        hour = current_datetime.hour
        if 5 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 18:
            time_period = "afternoon"
        else:
            time_period = "evening"
            
        # Generate intervention based on conditions and time period
        intervention = self._generate_intervention(conditions, time_period, current_datetime)
        
        # Log this intervention
        if intervention:
            self.intervention_history.append({
                "datetime": current_datetime,
                "intervention": intervention
            })
            
        return intervention
    
    def _get_recent_data(self, current_datetime: datetime) -> pd.DataFrame:
        """Get health data from the last 24 hours."""
        # Adjust date format to match the index
        start_time = current_datetime - timedelta(days=1)
        
        # Filter data to last 24 hours
        # Note: This assumes the data's datetime index is in a compatible format
        try:
            recent_data = self.health_data[
                (self.health_data.index >= pd.to_datetime(start_time)) & 
                (self.health_data.index <= pd.to_datetime(current_datetime))
            ]
            return recent_data
        except Exception as e:
            print(f"Error filtering recent data: {e}")
            # Return empty DataFrame if we can't filter
            return pd.DataFrame()
    
    def _detect_conditions(self, data: pd.DataFrame, current_datetime: datetime) -> Dict[str, bool]:
        """
        Analyze recent health data to detect various conditions.
        
        Returns:
            Dictionary of condition flags
        """
        conditions = {
            "high_heart_rate": False,
            "low_hrv": False,
            "poor_sleep_previous_night": False,
            "low_activity": False,
            "missed_mindfulness": False,
            "working_hours": False,
            "evening_wind_down": False
        }
        
        # Skip if no data
        if data.empty:
            return conditions
        
        # Check heart rate patterns
        try:
            recent_hr = data['Heart Rate (bpm)']
            if recent_hr.max() > 85:
                conditions["high_heart_rate"] = True
        except Exception:
            pass
            
        # Check HRV patterns
        try:
            recent_hrv = data['Heart Rate Variability (ms)']
            if recent_hrv.min() < 40:
                conditions["low_hrv"] = True
        except Exception:
            pass
            
        # Check sleep from previous night
        try:
            yesterday = (current_datetime - timedelta(days=1)).date()
            sleep_yesterday = data[data.index.date == yesterday]['Sleep Duration (hours)']
            deep_sleep_yesterday = data[data.index.date == yesterday]['Deep Sleep (%)']
            
            if not sleep_yesterday.empty and sleep_yesterday.iloc[0] < 6:
                conditions["poor_sleep_previous_night"] = True
            elif not deep_sleep_yesterday.empty and deep_sleep_yesterday.iloc[0] < 15:
                conditions["poor_sleep_previous_night"] = True
        except Exception:
            pass
            
        # Check activity level
        try:
            recent_steps = data['Step Count (steps)'].sum()
            if recent_steps < 3000:  # Arbitrary threshold
                conditions["low_activity"] = True
        except Exception:
            pass
            
        # Check mindfulness practice
        try:
            mindfulness_minutes = data['Mindfulness Minutes (minutes)'].sum()
            if mindfulness_minutes == 0:
                conditions["missed_mindfulness"] = True
        except Exception:
            pass
            
        # Check time-specific conditions
        hour = current_datetime.hour
        weekday = current_datetime.weekday()
        
        # Working hours (weekdays 9-5)
        if weekday < 5 and 9 <= hour < 17:
            conditions["working_hours"] = True
            
        # Evening wind-down (after 8pm)
        if hour >= 20:
            conditions["evening_wind_down"] = True
            
        return conditions
    
    def _generate_intervention(self, conditions: Dict[str, bool], time_period: str, 
                              current_datetime: datetime) -> Dict[str, Any]:
        """
        Generate appropriate intervention based on detected conditions.
        
        Args:
            conditions: Dictionary of detected health conditions
            time_period: Current time period (morning, afternoon, evening)
            current_datetime: Current date and time
            
        Returns:
            Dictionary with intervention details
        """
        # Check if we've already reached max interventions for today
        today = current_datetime.date()
        interventions_today = sum(1 for item in self.intervention_history 
                                if item["datetime"].date() == today)
        
        if interventions_today >= self.settings[self.persona_type]["max_daily_interventions"]:
            return None
            
        # Get priority interventions for this persona
        priority_interventions = self.settings[self.persona_type]["priority_interventions"]
        
        # Select intervention type based on conditions
        selected_intervention = None
        
        # High heart rate or low HRV -> breathing exercise
        if (conditions["high_heart_rate"] or conditions["low_hrv"]) and InterventionType.BREATHING in priority_interventions:
            selected_intervention = InterventionType.BREATHING
            
        # Missed mindfulness and evening -> mindfulness reminder
        elif conditions["missed_mindfulness"] and time_period == "evening" and InterventionType.MINDFULNESS in priority_interventions:
            selected_intervention = InterventionType.MINDFULNESS
            
        # Working hours -> work break reminder
        elif conditions["working_hours"] and InterventionType.WORK_BREAK in priority_interventions:
            selected_intervention = InterventionType.WORK_BREAK
            
        # Low activity -> physical activity suggestion
        elif conditions["low_activity"] and InterventionType.PHYSICAL in priority_interventions:
            selected_intervention = InterventionType.PHYSICAL
            
        # Poor sleep and evening -> sleep improvement
        elif conditions["poor_sleep_previous_night"] and time_period == "evening" and InterventionType.SLEEP in priority_interventions:
            selected_intervention = InterventionType.SLEEP
            
        # If nothing specific, choose random from priorities
        if not selected_intervention and priority_interventions:
            selected_intervention = random.choice(priority_interventions)
            
        # If we have an intervention, populate its content
        if selected_intervention:
            return self._create_intervention_content(selected_intervention, time_period)
        
        return None
    
    def _create_intervention_content(self, intervention_type: str, time_period: str) -> Dict[str, Any]:
        """Create the content for a specific intervention type."""
        intervention = {
            "type": intervention_type,
            "title": "",
            "description": "",
            "duration_minutes": 0,
            "notification_message": "",
            "time_period": time_period
        }
        
        # Breathing exercise
        if intervention_type == InterventionType.BREATHING:
            intervention["title"] = "Quick Breathing Reset"
            intervention["description"] = "Take 5 deep breaths: inhale for 4 counts, hold for 2, exhale for 6 counts."
            intervention["duration_minutes"] = 2
            intervention["notification_message"] = "Time for a quick breathing reset. Just 2 minutes can reduce tension."
            
        # Mindfulness session
        elif intervention_type == InterventionType.MINDFULNESS:
            intervention["title"] = "Evening Mindfulness Practice"
            intervention["description"] = "Find a quiet space. Focus on your breath for 5 minutes, noticing sensations without judgment."
            intervention["duration_minutes"] = 5
            intervention["notification_message"] = "Your scheduled mindfulness session is now. 5 minutes can improve your evening."
            
        # Physical activity
        elif intervention_type == InterventionType.PHYSICAL:
            intervention["title"] = "Movement Break"
            intervention["description"] = "Stand up, stretch your arms overhead, then touch your toes. Repeat 5 times."
            intervention["duration_minutes"] = 3
            intervention["notification_message"] = "Time to move! A quick 3-minute stretch can boost your energy."
            
        # Sleep improvement
        elif intervention_type == InterventionType.SLEEP:
            intervention["title"] = "Sleep Preparation Routine"
            intervention["description"] = "Dim lights, put devices away, and do gentle stretching for 10 minutes before bed."
            intervention["duration_minutes"] = 10
            intervention["notification_message"] = "Start winding down for better sleep. Your body needs quality rest tonight."
            
        # Work break
        elif intervention_type == InterventionType.WORK_BREAK:
            intervention["title"] = "Screen Break"
            intervention["description"] = "Look away from your screen. Focus on an object 20 feet away for 20 seconds."
            intervention["duration_minutes"] = 1
            intervention["notification_message"] = "Time for a quick screen break. Your eyes and mind need a moment of reset."
            
        # Hydration reminder  
        elif intervention_type == InterventionType.HYDRATION:
            intervention["title"] = "Hydration Reminder"
            intervention["description"] = "Drink a full glass of water (250ml)."
            intervention["duration_minutes"] = 1
            intervention["notification_message"] = "Hydration check! When did you last drink water? Take a minute to rehydrate."
            
        # Stress management
        elif intervention_type == InterventionType.STRESS_MANAGEMENT:
            intervention["title"] = "Stress Relief Moment"
            intervention["description"] = "Write down three things causing stress right now, then take three deep breaths for each one."
            intervention["duration_minutes"] = 5
            intervention["notification_message"] = "Notice feeling tense? Take 5 minutes for a quick stress-relief exercise."
            
        return intervention
        
    def get_daily_plan(self, target_date: datetime = None) -> List[Dict[str, Any]]:
        """
        Generate a daily plan of interventions.
        
        Args:
            target_date: The date to generate a plan for (defaults to today)
            
        Returns:
            List of intervention recommendations with scheduled times
        """
        if target_date is None:
            target_date = datetime.now()
            
        # Plan will contain interventions with scheduled times
        daily_plan = []
        
        # Get time ranges for each period from persona settings
        time_ranges = self.settings[self.persona_type]["optimal_intervention_times"]
        max_interventions = self.settings[self.persona_type]["max_daily_interventions"]
        
        # Determine how many interventions per time period
        interventions_per_period = max_interventions // len(time_ranges)
        remaining = max_interventions % len(time_ranges)
        
        # Distribute interventions across time periods
        for period, time_range in time_ranges.items():
            # Number of interventions for this period
            num_interventions = interventions_per_period
            if remaining > 0:
                num_interventions += 1
                remaining -= 1
                
            # Skip if no interventions for this period
            if num_interventions <= 0:
                continue
                
            # Get start and end times
            start_hour, start_min = time_range[0]
            end_hour, end_min = time_range[1]
            
            # Calculate duration in minutes
            start_mins = start_hour * 60 + start_min
            end_mins = end_hour * 60 + end_min
            duration_mins = end_mins - start_mins
            
            # Skip if invalid duration
            if duration_mins <= 0:
                continue
                
            # Divide the time period into equal intervals
            interval_mins = duration_mins // num_interventions
            
            # Generate interventions
            for i in range(num_interventions):
                # Calculate scheduled time
                schedule_mins = start_mins + (i * interval_mins) + (interval_mins // 2)
                hour = schedule_mins // 60
                minute = schedule_mins % 60
                
                # Create datetime for this intervention
                intervention_time = datetime(
                    target_date.year, target_date.month, target_date.day,
                    hour, minute
                )
                
                # Set up mock current time for recommendation
                mock_current_time = intervention_time - timedelta(minutes=5)
                
                # Generate recommendation
                recommendation = self.analyze_and_recommend(mock_current_time)
                
                # Add to plan if we got a recommendation
                if recommendation:
                    daily_plan.append({
                        "scheduled_time": intervention_time,
                        "intervention": recommendation
                    })
                    
        return daily_plan
        
    def display_intervention(self, intervention: Dict[str, Any]) -> None:
        """Display an intervention in a user-friendly format."""
        if not intervention:
            print("No intervention available.")
            return
            
        print("\n" + "="*50)
        print(f"🔔 {intervention['notification_message']}")
        print("-"*50)
        print(f"📌 {intervention['title']} ({intervention['duration_minutes']} minutes)")
        print(f"📝 {intervention['description']}")
        print("="*50 + "\n")
        
    def display_daily_plan(self, daily_plan: List[Dict[str, Any]]) -> None:
        """Display a full daily plan in a user-friendly format."""
        if not daily_plan:
            print("No interventions scheduled for today.")
            return
            
        print("\n" + "="*60)
        print(f"📅 DAILY WELLNESS PLAN FOR {daily_plan[0]['scheduled_time'].date()}")
        print(f"👤 Persona: {self.persona_type.capitalize()}")
        print("-"*60)
        
        for item in sorted(daily_plan, key=lambda x: x['scheduled_time']):
            time_str = item['scheduled_time'].strftime("%I:%M %p")
            intervention = item['intervention']
            print(f"⏰ {time_str}: {intervention['title']} ({intervention['duration_minutes']}m)")
            print(f"   {intervention['description']}")
            print()
            
        print("="*60 + "\n")


def simulate_day(health_data_path: str, persona_type: str):
    """Simulate a full day of interventions for a specific persona."""
    # Load health data
    health_data = load_health_data(health_data_path)
    if health_data is None:
        print(f"Failed to load health data from {health_data_path}")
        return
        
    # Initialize intervention system
    intervention_system = AdaptiveInterventionSystem(health_data, persona_type)
    
    # Get today's date
    today = datetime.now().date()
    
    # Generate daily plan
    daily_plan = intervention_system.get_daily_plan(datetime.now())
    
    # Display the plan
    intervention_system.display_daily_plan(daily_plan)
    
    print(f"\nSimulating real-time interventions throughout the day for {persona_type}...\n")
    
    # Simulate each hour of the day
    for hour in range(8, 23):  # 8 AM to 10 PM
        for minute in [0, 30]:  # Check twice per hour
            # Create current time
            current_time = datetime(today.year, today.month, today.day, hour, minute)
            
            # Get intervention recommendation
            recommendation = intervention_system.analyze_and_recommend(current_time)
            
            # Display if we got a recommendation
            if recommendation:
                print(f"At {current_time.strftime('%I:%M %p')}:")
                intervention_system.display_intervention(recommendation)


if __name__ == "__main__":
    # Define paths
    base_data_path = "Team27-Phish-and-Chips/LBG Reboot 2025 LDN - Health Demo Data"
    
    # Persona data mapping
    persona_data = {
        "samira": "2_samira_young_adult_mild_anxiety.csv",
        "javier": "3_javier_gen_z_student_academic_financial_stress.csv",
        "aisha": "4_aisha_young_adult_sleep_issues_low_activity.csv",
        "kofi": "5_kofi_young_professional_experiencing_burnout.csv",
        "ahmed": "6_ahmed_night_shift_worker_circadian_disruption.csv"
    }
    
    # Choose a persona to simulate
    selected_persona = "samira"  # Change to any of the available personas
    
    if selected_persona in persona_data:
        data_file = persona_data[selected_persona]
        data_path = os.path.join(base_data_path, data_file)
        
        print(f"Simulating interventions for: {selected_persona}")
        simulate_day(data_path, selected_persona)
    else:
        print(f"Persona '{selected_persona}' not found. Available personas: {', '.join(persona_data.keys())}") 