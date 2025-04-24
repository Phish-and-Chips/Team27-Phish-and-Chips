#!/bin/bash

# Variables
RESOURCE_GROUP="Team27"
LOCATION="westeurope"
ACR_NAME="youngadultsupportacr"
CONTAINER_APP_NAME="young-adult-support-api"
CONTAINER_APP_ENV="young-adult-support-env"

# # Create resource group
# echo "Creating resource group..."
# az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry (if it doesn't exist)
echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic 2>/dev/null || echo "ACR already exists"

# Enable admin user for ACR
az acr update --name $ACR_NAME --admin-enabled true

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# Build and push the Docker image to ACR
echo "Building and pushing Docker image to ACR..."
az acr build --registry $ACR_NAME --image young-adult-support-api:latest .

# Check if environment already exists
ENV_EXISTS=$(az containerapp env list --resource-group $RESOURCE_GROUP --query "[?name=='$CONTAINER_APP_ENV'].name" -o tsv)

if [ -z "$ENV_EXISTS" ]; then
  # List existing environments to potentially reuse one
  echo "You've reached the limit of 5 Container App Environments. Here are your existing environments:"
  az containerapp env list --query "[].{Name:name, ResourceGroup:resourceGroup}" -o table
  
  echo "Would you like to use an existing environment? Enter the name (or press enter to try cleanup):"
  read EXISTING_ENV
  
  if [ -n "$EXISTING_ENV" ]; then
    # Use existing environment
    CONTAINER_APP_ENV=$EXISTING_ENV
    echo "Using existing environment: $CONTAINER_APP_ENV"
  else
    # Try to find resource group of oldest environment to delete
    echo "Attempting to clean up an unused environment..."
    OLDEST_ENV=$(az containerapp env list --query "sort_by([],&createdTime)[0].{Name:name, ResourceGroup:resourceGroup}" -o json)
    if [ -n "$OLDEST_ENV" ]; then
      OLD_ENV_NAME=$(echo $OLDEST_ENV | jq -r '.Name')
      OLD_ENV_RG=$(echo $OLDEST_ENV | jq -r '.ResourceGroup')
      
      echo "Deleting oldest environment: $OLD_ENV_NAME in resource group $OLD_ENV_RG"
      az containerapp env delete --name $OLD_ENV_NAME --resource-group $OLD_ENV_RG --yes
      
      # Create new environment
      echo "Creating Container Apps environment..."
      az containerapp env create \
        --name $CONTAINER_APP_ENV \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION
    else
      echo "Could not find an environment to delete. Please manually delete an environment from the Azure portal."
      exit 1
    fi
  fi
else
  echo "Using existing Container Apps environment: $CONTAINER_APP_ENV"
fi

# Create Container App
echo "Creating Container App..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image ${ACR_NAME}.azurecr.io/young-adult-support-api:latest \
  --registry-server ${ACR_NAME}.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    DEPLOYMENT_NAME=$DEPLOYMENT_NAME

# Get the Container App URL
APP_URL=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
echo "Container App URL: https://$APP_URL" 