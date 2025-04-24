#!/bin/bash

# Variables
RESOURCE_GROUP="Team27"
LOCATION="westeurope"
APP_SERVICE_PLAN="young-adult-support-plan"
APP_NAME="young-adult-support-api"

# Create resource group
# echo "Creating resource group..."
# az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan
echo "Creating App Service Plan..."
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create Web App
echo "Creating Web App..."
az webapp create --name $APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.10"

# Set environment variables
echo "Setting environment variables..."
az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings \
  AZURE_OPENAI_KEY="$AZURE_OPENAI_KEY" \
  AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
  DEPLOYMENT_NAME="$DEPLOYMENT_NAME" \
  WEBSITES_PORT=8000

# Configure the startup command
echo "Setting startup command..."
az webapp config set --name $APP_NAME --resource-group $RESOURCE_GROUP --startup-file "gunicorn agen:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"

# Deploy code from local git
echo "Deploying code..."
az webapp deployment source config-local-git --name $APP_NAME --resource-group $RESOURCE_GROUP

# Get the git deployment URL
GIT_URL=$(az webapp deployment source config-local-git --name $APP_NAME --resource-group $RESOURCE_GROUP --query url -o tsv)
echo "Git deployment URL: $GIT_URL"

echo "Deployment setup complete. Add the remote git repository and push your code:"
echo "git remote add azure $GIT_URL"
echo "git push azure main" 