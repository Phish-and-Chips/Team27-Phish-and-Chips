"""
Financial Guidance Agent

This component provides financial guidance and recommendations to young adults.
"""

import os
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple

# Constants for financial thresholds
MIN_EMERGENCY_FUND = 3000  # Minimum emergency fund in GBP
MAX_DEBT_TO_INCOME = 0.36  # Maximum debt-to-income ratio

class FinancialProfile:
    """Class to represent a user's financial profile."""
    
    def __init__(self, 
                 monthly_income: float,
                 fixed_expenses: float,
                 variable_expenses: float,
                 savings: float,
                 debt: float,
                 financial_goals: List[Dict[str, Any]] = None):
        """
        Initialize financial profile with basic information.
        
        Args:
            monthly_income: Monthly income in GBP
            fixed_expenses: Fixed monthly expenses (rent, bills) in GBP
            variable_expenses: Variable monthly expenses (food, entertainment) in GBP
            savings: Current savings in GBP
            debt: Current total debt in GBP
            financial_goals: List of financial goals with amount and target date
        """
        self.monthly_income = monthly_income
        self.fixed_expenses = fixed_expenses
        self.variable_expenses = variable_expenses
        self.savings = savings
        self.debt = debt
        self.financial_goals = financial_goals or []
        
        # Calculate derived metrics
        self.disposable_income = self.monthly_income - self.fixed_expenses - self.variable_expenses
        self.debt_to_income_ratio = self.debt / (self.monthly_income * 12) if self.monthly_income > 0 else float('inf')
        self.months_emergency_fund = self.savings / (self.fixed_expenses + self.variable_expenses) if (self.fixed_expenses + self.variable_expenses) > 0 else 0
    
    def get_financial_health_score(self) -> Tuple[int, Dict[str, Any]]:
        """
        Calculate overall financial health score out of 100.
        
        Returns:
            Tuple of (score, breakdown_dict)
        """
        score = 0
        breakdown = {}
        
        # Emergency fund (0-25 points)
        if self.months_emergency_fund >= 6:
            fund_score = 25
        elif self.months_emergency_fund >= 3:
            fund_score = 15
        elif self.months_emergency_fund >= 1:
            fund_score = 10
        else:
            fund_score = 0
        score += fund_score
        breakdown["emergency_fund"] = {
            "score": fund_score, 
            "max": 25,
            "months": self.months_emergency_fund
        }
        
        # Debt-to-income ratio (0-25 points)
        if self.debt_to_income_ratio <= 0.1:
            debt_score = 25
        elif self.debt_to_income_ratio <= 0.3:
            debt_score = 20
        elif self.debt_to_income_ratio <= 0.4:
            debt_score = 10
        elif self.debt_to_income_ratio <= 0.5:
            debt_score = 5
        else:
            debt_score = 0
        score += debt_score
        breakdown["debt_ratio"] = {
            "score": debt_score, 
            "max": 25,
            "ratio": self.debt_to_income_ratio
        }
        
        # Savings rate (0-25 points)
        savings_rate = self.disposable_income / self.monthly_income if self.monthly_income > 0 else 0
        if savings_rate >= 0.2:
            savings_score = 25
        elif savings_rate >= 0.1:
            savings_score = 15
        elif savings_rate > 0:
            savings_score = 5
        else:
            savings_score = 0
        score += savings_score
        breakdown["savings_rate"] = {
            "score": savings_score, 
            "max": 25,
            "rate": savings_rate
        }
        
        # Budget balance (0-25 points)
        if self.disposable_income > 0.2 * self.monthly_income:
            budget_score = 25
        elif self.disposable_income > 0.1 * self.monthly_income:
            budget_score = 20
        elif self.disposable_income > 0:
            budget_score = 15
        elif self.disposable_income == 0:
            budget_score = 5
        else:
            budget_score = 0
        score += budget_score
        breakdown["budget_balance"] = {
            "score": budget_score, 
            "max": 25,
            "disposable_income": self.disposable_income
        }
        
        return score, breakdown


class FinancialGuidanceAgent:
    """Agent that provides financial guidance based on a user's profile."""
    
    def __init__(self, persona_type: str = None):
        """
        Initialize the financial guidance agent.
        
        Args:
            persona_type: Type of persona (e.g., "student", "young_professional")
        """
        self.persona_type = persona_type
        
        # Create dummy financial profiles for our personas
        self.persona_profiles = {
            "samira": FinancialProfile(
                monthly_income=3500,  # Backend developer at a London fintech
                fixed_expenses=1200,  # Shared flat with roommates
                variable_expenses=1000,
                savings=4500,
                debt=5000,  # Family loan
                financial_goals=[
                    {"name": "Pay off family loan", "amount": 5000, "target_date": date(2025, 12, 31)}
                ]
            ),
            "javier": FinancialProfile(
                monthly_income=1100,  # Part-time job while studying
                fixed_expenses=350,  # Rent
                variable_expenses=500,  # Including textbooks
                savings=800,
                debt=2500,  # Student debt
                financial_goals=[
                    {"name": "Emergency fund", "amount": 1500, "target_date": date(2025, 8, 31)}
                ]
            ),
            "aisha": FinancialProfile(
                monthly_income=2200,  # Freelance illustrator with variable income
                fixed_expenses=800,  # Bristol rent
                variable_expenses=900,
                savings=1800,
                debt=1200,
                financial_goals=[
                    {"name": "Build stable income", "amount": 3000, "target_date": date(2025, 6, 30)}
                ]
            ),
            "kofi": FinancialProfile(
                monthly_income=4000,  # Marketing strategist
                fixed_expenses=1800,  # Rent with partner in Shoreditch
                variable_expenses=1400,
                savings=32000,  # Home deposit savings
                debt=3000,
                financial_goals=[
                    {"name": "House deposit", "amount": 50000, "target_date": date(2026, 12, 31)}
                ]
            ),
            "ahmed": FinancialProfile(
                monthly_income=2800,  # ICU nurse with shift work
                fixed_expenses=950,  # Shared house in Manchester
                variable_expenses=1100,
                savings=3500,
                debt=2200,
                financial_goals=[
                    {"name": "Career development fund", "amount": 5000, "target_date": date(2026, 3, 31)}
                ]
            ),
        }
        
    def get_profile(self, persona_type: str = None) -> Optional[FinancialProfile]:
        """Get the financial profile for a specific persona."""
        persona = persona_type or self.persona_type
        if not persona or persona not in self.persona_profiles:
            return None
        return self.persona_profiles[persona]
    
    def analyze_financial_health(self, profile: FinancialProfile = None, persona_type: str = None) -> Dict[str, Any]:
        """
        Analyze the financial health of a profile or a specific persona.
        
        Args:
            profile: Financial profile to analyze (optional)
            persona_type: Persona type to analyze if profile not provided
            
        Returns:
            Dictionary with analysis results
        """
        if profile is None:
            profile = self.get_profile(persona_type)
            if profile is None:
                return {"error": "No valid profile or persona provided"}
                
        # Get health score
        score, breakdown = profile.get_financial_health_score()
        
        # Generate key insights
        insights = []
        recommendations = []
        
        # Emergency fund insights
        if profile.months_emergency_fund < 3:
            insights.append({
                "category": "emergency_fund",
                "severity": "high" if profile.months_emergency_fund < 1 else "medium",
                "message": f"Your emergency fund would only last {profile.months_emergency_fund:.1f} months"
            })
            recommendations.append({
                "category": "emergency_fund",
                "action": "Build emergency fund",
                "description": f"Aim to save £{MIN_EMERGENCY_FUND} or 3-6 months of expenses",
                "priority": "high" if profile.months_emergency_fund < 1 else "medium"
            })
        
        # Debt insights
        if profile.debt_to_income_ratio > MAX_DEBT_TO_INCOME:
            insights.append({
                "category": "debt",
                "severity": "high",
                "message": f"Your debt-to-income ratio is {profile.debt_to_income_ratio:.2f}, above the recommended maximum of {MAX_DEBT_TO_INCOME}"
            })
            recommendations.append({
                "category": "debt",
                "action": "Reduce debt burden",
                "description": "Focus on paying down high-interest debt first",
                "priority": "high"
            })
        
        # Budget insights
        if profile.disposable_income < 0:
            insights.append({
                "category": "budget",
                "severity": "high",
                "message": f"You're spending £{abs(profile.disposable_income):.2f} more than you earn each month"
            })
            recommendations.append({
                "category": "budget",
                "action": "Reduce expenses",
                "description": "Find areas to cut back on non-essential spending",
                "priority": "high"
            })
        elif profile.disposable_income < profile.monthly_income * 0.1:
            insights.append({
                "category": "budget",
                "severity": "medium",
                "message": f"Your disposable income is only {(profile.disposable_income / profile.monthly_income * 100):.1f}% of your income"
            })
            recommendations.append({
                "category": "budget",
                "action": "Optimize budget",
                "description": "Look for ways to reduce expenses to increase savings rate",
                "priority": "medium"
            })
            
        # Additional persona-specific insights
        if persona_type == "javier":
            insights.append({
                "category": "student_finance",
                "severity": "medium",
                "message": "As a student, your income fluctuates with term-time work"
            })
            recommendations.append({
                "category": "student_finance",
                "action": "Build term-end buffer",
                "description": "Save extra during work periods to cover term-end expenses",
                "priority": "medium"
            })
        elif persona_type == "aisha":
            insights.append({
                "category": "variable_income",
                "severity": "medium",
                "message": "Your freelance income varies month to month, creating planning challenges"
            })
            recommendations.append({
                "category": "variable_income",
                "action": "Income smoothing",
                "description": "Set aside a percentage of high-income months to supplement lower months",
                "priority": "high"
            })
            
        return {
            "score": score,
            "breakdown": breakdown,
            "insights": insights,
            "recommendations": recommendations,
            "profile_summary": {
                "monthly_income": profile.monthly_income,
                "fixed_expenses": profile.fixed_expenses,
                "variable_expenses": profile.variable_expenses,
                "disposable_income": profile.disposable_income,
                "savings": profile.savings,
                "debt": profile.debt,
                "months_emergency_fund": profile.months_emergency_fund,
                "debt_to_income_ratio": profile.debt_to_income_ratio
            }
        }
        
    def get_financial_education_resources(self, categories: List[str] = None) -> List[Dict[str, str]]:
        """
        Return relevant financial education resources.
        
        Args:
            categories: List of resource categories to return
        
        Returns:
            List of resource dictionaries
        """
        all_resources = {
            "budgeting": [
                {
                    "title": "50-30-20 Budgeting Method",
                    "description": "A simple way to allocate your income: 50% on needs, 30% on wants, 20% on savings and debt repayment.",
                    "url": "https://www.moneyhelper.org.uk/en/everyday-money/budgeting/how-to-make-a-budget"
                },
                {
                    "title": "Budget Planner Tool",
                    "description": "Interactive tool to track income and expenses, helping to identify areas for saving.",
                    "url": "https://www.moneyhelper.org.uk/en/everyday-money/budgeting/budget-planner"
                }
            ],
            "debt_management": [
                {
                    "title": "Debt Snowball Method",
                    "description": "Pay off debts starting with the smallest balance to create momentum.",
                    "url": "https://www.moneyhelper.org.uk/en/everyday-money/credit-and-purchases/how-to-prioritise-your-debts"
                },
                {
                    "title": "Free Debt Advice",
                    "description": "Where to get free advice on managing debt in the UK.",
                    "url": "https://www.stepchange.org/"
                }
            ],
            "saving": [
                {
                    "title": "Emergency Fund Basics",
                    "description": "How to build and maintain an emergency fund to cover unexpected expenses.",
                    "url": "https://www.moneyhelper.org.uk/en/savings/types-of-savings/emergency-savings-how-much-is-enough"
                },
                {
                    "title": "Automatic Savings Apps",
                    "description": "Apps that automatically set aside small amounts to build savings without effort.",
                    "url": "https://www.moneysavingexpert.com/banking/auto-saving-apps/"
                }
            ],
            "investing": [
                {
                    "title": "Investment Basics for Beginners",
                    "description": "Simple guide to getting started with investing small amounts.",
                    "url": "https://www.moneyhelper.org.uk/en/savings/investing/investing-beginners-guide"
                },
                {
                    "title": "Stocks & Shares ISAs Explained",
                    "description": "Tax-efficient investment accounts available in the UK.",
                    "url": "https://www.moneysavingexpert.com/savings/stocks-shares-isas/"
                }
            ],
            "student_finance": [
                {
                    "title": "Student Budget Calculator",
                    "description": "Tool to help students plan term-time finances.",
                    "url": "https://www.savethestudent.org/money/student-budgeting/student-budget-calculator.html"
                },
                {
                    "title": "Student Banking Guide",
                    "description": "Choosing the right student bank account with overdraft facilities.",
                    "url": "https://www.moneysavingexpert.com/students/student-bank-account/"
                }
            ],
            "variable_income": [
                {
                    "title": "Budgeting with Irregular Income",
                    "description": "Techniques for financial planning when income fluctuates.",
                    "url": "https://www.moneyhelper.org.uk/en/everyday-money/budgeting/how-to-budget-with-an-irregular-income"
                },
                {
                    "title": "Freelancer Financial Planning",
                    "description": "Tax and income smoothing strategies for freelancers.",
                    "url": "https://www.ipse.co.uk/advice/financial-wellbeing"
                }
            ]
        }
        
        if not categories:
            # Return one from each category if no specific categories requested
            result = []
            for category, resources in all_resources.items():
                result.append(resources[0])
            return result
            
        # Return requested categories
        result = []
        for category in categories:
            if category in all_resources:
                result.extend(all_resources[category])
        return result
    
    def get_insurance_recommendations(self, persona_type: str = None) -> List[Dict[str, Any]]:
        """
        Provide insurance recommendations based on persona type.
        
        Args:
            persona_type: Type of persona for tailored recommendations
            
        Returns:
            List of insurance product recommendations
        """
        persona = persona_type or self.persona_type
        
        # Base recommendations for young adults
        base_recommendations = [
            {
                "type": "Contents Insurance",
                "priority": "medium",
                "description": "Protects your belongings in rented accommodation",
                "estimated_cost": "£10-15 per month",
                "key_providers": ["Aviva", "Churchill", "Direct Line"]
            },
            {
                "type": "Income Protection",
                "priority": "medium",
                "description": "Provides income if you're unable to work due to illness or injury",
                "estimated_cost": "£20-40 per month depending on occupation",
                "key_providers": ["Aviva", "LV=", "Vitality"]
            }
        ]
        
        # Persona-specific additions
        persona_specific = []
        
        if persona == "javier":  # Student
            persona_specific = [
                {
                    "type": "Gadget Insurance",
                    "priority": "high",
                    "description": "Cover for laptop and devices essential for studying",
                    "estimated_cost": "£8-12 per month",
                    "key_providers": ["Protect Your Bubble", "Insurance2Go", "CoverCloud"]
                }
            ]
        elif persona == "aisha":  # Freelancer
            persona_specific = [
                {
                    "type": "Professional Indemnity Insurance",
                    "priority": "high",
                    "description": "Protection against claims from clients for professional mistakes",
                    "estimated_cost": "£15-25 per month for basic cover",
                    "key_providers": ["Hiscox", "Simply Business", "Superscript"]
                }
            ]
        elif persona == "kofi":  # Higher income with partner
            persona_specific = [
                {
                    "type": "Life Insurance",
                    "priority": "medium",
                    "description": "Provides financial support to dependents if you die",
                    "estimated_cost": "£10-20 per month",
                    "key_providers": ["Legal & General", "Aviva", "Royal London"]
                }
            ]
        elif persona == "ahmed":  # Healthcare worker
            persona_specific = [
                {
                    "type": "Critical Illness Cover",
                    "priority": "high",
                    "description": "Pays a lump sum if diagnosed with specific serious illnesses",
                    "estimated_cost": "£25-40 per month",
                    "key_providers": ["Aviva", "Zurich", "AIG"]
                }
            ]
            
        return base_recommendations + persona_specific
    
    def display_financial_analysis(self, persona_type: str = None):
        """Display financial analysis for a specific persona in a formatted way."""
        persona = persona_type or self.persona_type
        if not persona:
            print("Error: No persona specified")
            return
            
        profile = self.get_profile(persona)
        if not profile:
            print(f"Error: No profile found for persona '{persona}'")
            return
            
        analysis = self.analyze_financial_health(profile, persona)
        score = analysis["score"]
        
        print("\n" + "="*60)
        print(f"📊 FINANCIAL HEALTH ANALYSIS FOR: {persona.capitalize()}")
        print("-"*60)
        
        # Overall score
        print(f"Overall Financial Health Score: {score}/100")
        if score >= 80:
            print("🟢 EXCELLENT: Your finances are in great shape!")
        elif score >= 60:
            print("🟡 GOOD: You're on the right track with some areas to improve.")
        elif score >= 40:
            print("🟠 FAIR: Several areas need attention to improve financial health.")
        else:
            print("🔴 NEEDS ATTENTION: Immediate action required to address financial challenges.")
            
        # Profile summary
        print("\n📝 FINANCIAL PROFILE:")
        summary = analysis["profile_summary"]
        print(f"• Monthly Income: £{summary['monthly_income']:.2f}")
        print(f"• Fixed Expenses: £{summary['fixed_expenses']:.2f}")
        print(f"• Variable Expenses: £{summary['variable_expenses']:.2f}")
        print(f"• Disposable Income: £{summary['disposable_income']:.2f}")
        print(f"• Savings: £{summary['savings']:.2f}")
        print(f"• Debt: £{summary['debt']:.2f}")
        print(f"• Emergency Fund Duration: {summary['months_emergency_fund']:.1f} months")
        print(f"• Debt-to-Income Ratio: {summary['debt_to_income_ratio']:.2f}")
        
        # Key insights
        print("\n🔍 KEY INSIGHTS:")
        for insight in analysis["insights"]:
            prefix = "❗" if insight["severity"] == "high" else "⚠️" if insight["severity"] == "medium" else "ℹ️"
            print(f"{prefix} {insight['message']}")
            
        # Recommendations
        print("\n🎯 RECOMMENDATIONS:")
        for rec in analysis["recommendations"]:
            prefix = "❗" if rec["priority"] == "high" else "⚠️" if rec["priority"] == "medium" else "ℹ️"
            print(f"{prefix} {rec['action']}: {rec['description']}")
            
        # Resources
        categories = [rec["category"] for rec in analysis["recommendations"]]
        resources = self.get_financial_education_resources(categories)
        
        print("\n📚 RECOMMENDED RESOURCES:")
        for resource in resources:
            print(f"• {resource['title']}: {resource['description']}")
            print(f"  Link: {resource['url']}")
            
        # Insurance
        insurance = self.get_insurance_recommendations(persona)
        
        print("\n🛡️ INSURANCE RECOMMENDATIONS:")
        for ins in insurance:
            prefix = "❗" if ins["priority"] == "high" else "⚠️" if ins["priority"] == "medium" else "ℹ️"
            print(f"{prefix} {ins['type']}: {ins['description']}")
            print(f"  Estimated cost: {ins['estimated_cost']}")
            print(f"  Key providers: {', '.join(ins['key_providers'])}")
            
        print("="*60 + "\n")


if __name__ == "__main__":
    # Create a financial guidance agent
    agent = FinancialGuidanceAgent()
    
    # Test with different personas
    personas = ["samira", "javier", "aisha", "kofi", "ahmed"]
    
    # Choose a persona to analyze
    selected_persona = "samira"  # Change to any of the available personas
    
    if selected_persona in personas:
        print(f"Analyzing financial health for: {selected_persona}")
        agent.display_financial_analysis(selected_persona)
    else:
        print(f"Persona '{selected_persona}' not found. Available personas: {', '.join(personas)}") 