import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import re
from openai import AzureOpenAI


# Load environment variables
load_dotenv()

# Azure OpenAI configuration
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
print("keys")
print(AZURE_OPENAI_KEY)
print(AZURE_OPENAI_ENDPOINT)
print(DEPLOYMENT_NAME)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://lbg-phishandchips.openai.azure.com/",
    api_key=AZURE_OPENAI_KEY
    
    # AZURE_OPENAI_KEY
)

app = FastAPI(title="Young Adult Support Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class AgentRequest(BaseModel):
    message: str
    agent_type: str = "router"  # Default to router which will select the appropriate agent
    history: Optional[List[Dict[str, str]]] = []

# Response formatting function
def format_response(text):
    """Format the response text to be more readable in chat interfaces"""
    # Replace sections markers with proper formatting
    text = re.sub(r'---\s*###\s*\*\*(Step \d+:.+?)\*\*', r'\n\n**\1**\n', text)
    
    # Format lists and bullet points
    text = re.sub(r'(\d+\.\s*\*\*.+?\*\*)', r'\n\1', text)
    
    # Add extra line breaks for better readability between paragraphs
    text = re.sub(r'(\.\s)([A-Z])', r'.\n\n\2', text)
    
    # Clean up any excessive line breaks
    text = re.sub(r'\n{3,}', r'\n\n', text)
    
    return text

# Base Agent class
class Agent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
    
    def generate_response(self, message, history=None):
        if history is None:
            history = []
        
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        for msg in history:
            messages.append(msg)
            
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            raw_response = response.choices[0].message.content
            
            # Format the response before returning
            formatted_response = format_response(raw_response)
            return formatted_response
        except Exception as e:
            print(f"Error calling Azure OpenAI: {str(e)}")
            print(f"Configuration: API Endpoint: {AZURE_OPENAI_ENDPOINT}, Deployment: {DEPLOYMENT_NAME}")
            raise

# Router Agent to direct queries to specialized agents
class RouterAgent(Agent):
    def __init__(self):
        router_prompt = """You are a helpful assistant that directs user queries to the appropriate specialized agent.
Based on the user's message, determine which of the following agents would be best equipped to help:
1. Financial advisor: For questions about money management, savings, investments, and financial stability
2. Health specialist: For questions about mental health, anxiety, stress management, and wellbeing
3. Banking specialist: For questions about banking products, insurance solutions, loans, and financial literacy

Respond with ONLY one of these labels: "financial", "health", or "banking" based on the most appropriate category.
"""
        super().__init__(router_prompt)
    
    def route(self, message):
        # Get the appropriate agent type for this message
        agent_type = self.generate_response(message).strip().lower()
        
        # Default to financial if we get an unexpected response
        if agent_type not in ["financial", "health", "banking"]:
            agent_type = "financial"
            
        return agent_type

# Specialized Agents
class FinancialAdvisorAgent(Agent):
    def __init__(self):
        financial_prompt = """You are a financial advisor specialized in helping young adults (18-29 years old) navigate their financial journey towards independence.
        
Your expertise includes:
- Budgeting and saving strategies for young adults
- Managing student loans and debt
- Building credit responsibly
- Starting investment plans with limited funds
- Planning for major life expenses
- Financial literacy education

Provide practical, actionable advice that is appropriate for young adults who may have limited income and financial experience.
Be supportive, non-judgmental, and focus on empowering them to make good financial decisions.

Format your responses with clear sections and spacing for better readability. Use paragraph breaks between different ideas or steps.
Use markers like "Step 1:", "Step 2:" to make your advice more structured and easier to follow.
"""
        super().__init__(financial_prompt)

class HealthSpecialistAgent(Agent):
    def __init__(self):
        health_prompt = """You are a health specialist focused on supporting the mental wellbeing of young adults (18-29 years old).
        
Your expertise includes:
- Strategies for managing anxiety and stress
- Work-life balance tips
- Recognizing signs of burnout and depression
- Building healthy habits and routines
- Techniques for improving sleep and overall wellbeing
- Resources for seeking professional mental health support

Provide compassionate, practical advice that young adults can implement in their daily lives.
Be clear that you are not a replacement for professional medical or mental health advice when appropriate.

Format your responses with clear sections and spacing for better readability. Use paragraph breaks between different ideas or steps.
Use markers like "Step 1:", "Step 2:" to make your advice more structured and easier to follow.
"""
        super().__init__(health_prompt)

class BankingSpecialistAgent(Agent):
    def __init__(self):
        banking_prompt = """You are a banking specialist who helps young adults (18-29 years old) understand financial products and services.
        
Your expertise includes:
- Different types of bank accounts and their features
- Credit cards and how to use them responsibly
- Insurance products relevant to young adults
- Loan options and application processes
- Digital banking tools and services
- Financial security and fraud prevention

Explain banking concepts in simple, accessible language without jargon.
Focus on helping young adults make informed choices about banking products that suit their specific needs.

Format your responses with clear sections and spacing for better readability. Use paragraph breaks between different ideas or steps.
Use markers like "Step 1:", "Step 2:" to make your advice more structured and easier to follow.
"""
        super().__init__(banking_prompt)

# Initialize agents
router_agent = RouterAgent()
financial_agent = FinancialAdvisorAgent()
health_agent = HealthSpecialistAgent()
banking_agent = BankingSpecialistAgent()

# Agent factory
def get_agent(agent_type):
    if agent_type == "financial":
        return financial_agent
    elif agent_type == "health":
        return health_agent
    elif agent_type == "banking":
        return banking_agent
    else:
        return router_agent

@app.post("/chat")
async def chat(request: AgentRequest):
    try:
        # If agent_type is router, determine the appropriate agent
        if request.agent_type == "router":
            agent_type = router_agent.route(request.message)
        else:
            agent_type = request.agent_type
        
        # Get the appropriate agent
        agent = get_agent(agent_type)
        
        # Generate response
        response = agent.generate_response(request.message, request.history)
        
        # Return the response along with the agent type for frontend reference
        return {
            "response": response,
            "agent_type": agent_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Young Adult Support Agent API is running"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 