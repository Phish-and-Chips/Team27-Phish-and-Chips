"""
Young Adult Support System - Main Application

This script integrates all components of the support system and provides
a simple command-line interface to interact with the system.
"""

import os
import sys
from datetime import datetime
import pandas as pd

# Import components
from health_monitor import load_health_data, analyze_samira_data
from intervention_system import AdaptiveInterventionSystem, simulate_day
from financial_guidance import FinancialGuidanceAgent

class YoungAdultSupportSystem:
    """Main system that integrates all components."""
    
    def __init__(self):
        """Initialize the support system and its components."""
        self.base_data_path = "Team27-Phish-and-Chips/LBG Reboot 2025 LDN - Health Demo Data"
        
        # Persona data mapping
        self.persona_data = {
            "samira": "2_samira_young_adult_mild_anxiety.csv",
            "javier": "3_javier_gen_z_student_academic_financial_stress.csv",
            "aisha": "4_aisha_young_adult_sleep_issues_low_activity.csv",
            "kofi": "5_kofi_young_professional_experiencing_burnout.csv",
            "ahmed": "6_ahmed_night_shift_worker_circadian_disruption.csv"
        }
        
        # Persona descriptions for reference
        self.persona_descriptions = {
            "samira": "28-year-old backend developer at a London fintech with mild anxiety.",
            "javier": "21-year-old media student in Manchester with academic and financial stress.",
            "aisha": "30-year-old freelance illustrator in Bristol with sleep issues and low activity.",
            "kofi": "33-year-old marketing strategist in Shoreditch experiencing burnout.",
            "ahmed": "26-year-old ICU nurse in Manchester with circadian disruption from night shifts."
        }
        
        # Initialize components
        self.financial_agent = FinancialGuidanceAgent()
        
        # The health data and intervention system will be initialized per persona
        self.health_data = None
        self.intervention_system = None
        self.active_persona = None
        
    def select_persona(self, persona_name: str):
        """
        Select and load a specific persona.
        
        Args:
            persona_name: Name of the persona to load
        
        Returns:
            bool: Success status
        """
        if persona_name not in self.persona_data:
            print(f"Error: Persona '{persona_name}' not found.")
            return False
            
        # Load health data for this persona
        data_file = self.persona_data[persona_name]
        data_path = os.path.join(self.base_data_path, data_file)
        
        self.health_data = load_health_data(data_path)
        if self.health_data is None:
            return False
            
        # Initialize the intervention system with this persona's data
        self.intervention_system = AdaptiveInterventionSystem(self.health_data, persona_name)
        
        self.active_persona = persona_name
        return True
        
    def show_persona_list(self):
        """Display the list of available personas with descriptions."""
        print("\n=== Available Personas ===")
        for name, description in self.persona_descriptions.items():
            print(f"- {name}: {description}")
            
    def run_health_analysis(self):
        """Run health data analysis for the active persona."""
        if not self.active_persona or self.health_data is None:
            print("Error: No active persona selected.")
            return
            
        print(f"\n=== Health Analysis for {self.active_persona.capitalize()} ===")
        # Currently only Samira has a specific analysis function
        if self.active_persona == "samira":
            analyze_samira_data(self.health_data)
        else:
            print(f"Detailed analysis for {self.active_persona} is not yet implemented.")
            print("Basic statistics:")
            print(f"Total records: {len(self.health_data)}")
            print(f"Date range: {self.health_data.index.min().date()} to {self.health_data.index.max().date()}")
            print("\nSample health data:")
            print(self.health_data.head(3))
            
    def run_intervention_simulation(self):
        """Run a simulation of the intervention system for the active persona."""
        if not self.active_persona or self.intervention_system is None:
            print("Error: No active persona selected.")
            return
            
        print(f"\n=== Intervention Simulation for {self.active_persona.capitalize()} ===")
        
        # Generate daily plan
        daily_plan = self.intervention_system.get_daily_plan(datetime.now())
        
        # Display the plan
        self.intervention_system.display_daily_plan(daily_plan)
        
        # Sample interventions
        print("\nSample real-time interventions:")
        for hour in [10, 14, 17, 21]:  # Sample hours throughout the day
            current_time = datetime.now().replace(hour=hour, minute=0)
            recommendation = self.intervention_system.analyze_and_recommend(current_time)
            if recommendation:
                print(f"\nAt {current_time.strftime('%I:%M %p')}:")
                self.intervention_system.display_intervention(recommendation)
            
    def run_financial_guidance(self):
        """Run financial guidance for the active persona."""
        if not self.active_persona:
            print("Error: No active persona selected.")
            return
            
        self.financial_agent.display_financial_analysis(self.active_persona)
        
    def run_full_demo(self):
        """Run a full demonstration of all components for the active persona."""
        if not self.active_persona:
            print("Error: No active persona selected.")
            return
            
        print(f"\n{'='*20} FULL SYSTEM DEMO FOR {self.active_persona.upper()} {'='*20}")
        print(f"Persona: {self.active_persona.capitalize()} - {self.persona_descriptions[self.active_persona]}")
        
        # Run health analysis
        print("\n[1/3] HEALTH DATA ANALYSIS")
        self.run_health_analysis()
        
        # Run intervention system
        print("\n[2/3] ADAPTIVE INTERVENTION SYSTEM")
        self.run_intervention_simulation()
        
        # Run financial guidance
        print("\n[3/3] FINANCIAL GUIDANCE SYSTEM")
        self.run_financial_guidance()
        
        print(f"\n{'='*70}")
        print("Demo complete. This represents a day in the life of using our system.")
        print("In a real implementation, these components would be integrated into a")
        print("mobile application with real-time monitoring and personalized guidance.")
        
    def run_interactive_menu(self):
        """Run an interactive command-line menu."""
        while True:
            print("\n==== Young Adult Support System ====")
            if self.active_persona:
                print(f"Active Persona: {self.active_persona}")
            else:
                print("No persona selected")
                
            print("\nMenu Options:")
            print("1. Select Persona")
            print("2. Run Health Analysis")
            print("3. Run Intervention Simulation")
            print("4. Run Financial Guidance")
            print("5. Run Full System Demo")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.show_persona_list()
                persona = input("\nEnter persona name: ").lower()
                self.select_persona(persona)
            elif choice == '2':
                self.run_health_analysis()
            elif choice == '3':
                self.run_intervention_simulation()
            elif choice == '4':
                self.run_financial_guidance()
            elif choice == '5':
                self.run_full_demo()
            elif choice == '6':
                print("\nExiting the system. Thank you!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    # Check if we have the required files
    required_files = [
        "health_monitor.py",
        "intervention_system.py",
        "financial_guidance.py"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(os.path.join("Team27-Phish-and-Chips", f))]
    
    if missing_files:
        print("Error: The following required files are missing:")
        for file in missing_files:
            print(f"- {file}")
        print("\nPlease ensure all component files are in the correct location.")
        sys.exit(1)
    
    # Create and run the system
    system = YoungAdultSupportSystem()
    
    # Check if a persona name was provided as a command-line argument
    if len(sys.argv) > 1 and sys.argv[1] in system.persona_data:
        # Run a demo with the specified persona
        system.select_persona(sys.argv[1])
        system.run_full_demo()
    else:
        # Run the interactive menu
        system.run_interactive_menu() 