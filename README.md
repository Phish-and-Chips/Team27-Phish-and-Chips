# Young Adult Support Agent API

A FastAPI application that uses Azure OpenAI to power specialized AI agents for financial advice, health support, and banking assistance.

## Local Development

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   AZURE_OPENAI_KEY=your_azure_openai_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   DEPLOYMENT_NAME=your_deployment_name
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   uvicorn agen:app --reload
   ```

## Azure Deployment Options

### Option 1: Azure App Service

Deploy using the provided script:

```bash
# Make the script executable
chmod +x azure-deploy.sh

# Set your Azure OpenAI variables
export AZURE_OPENAI_KEY=your_azure_openai_key
export AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
export DEPLOYMENT_NAME=your_deployment_name

# Run the deployment script
./azure-deploy.sh
```

### Option 2: Azure Container App

Deploy as a containerized application:

```bash
# Make the script executable
chmod +x azure-container-deploy.sh

# Set your Azure OpenAI variables
export AZURE_OPENAI_KEY=your_azure_openai_key
export AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
export DEPLOYMENT_NAME=your_deployment_name

# Run the container deployment script
./azure-container-deploy.sh
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /chat`: Main endpoint for chatting with specialized agents

### Chat Request Format
```json
{
  "message": "How can I manage my student loans?",
  "agent_type": "router",
  "history": []
}
```

### Chat Response Format
```json
{
  "response": "To manage your student loans effectively...",
  "agent_type": "financial"
}
``` 