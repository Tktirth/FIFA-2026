#!/bin/bash
set -e

# Configuration
PROJECT_ID=$1
REGION=${2:-us-central1}

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: ./deploy.sh <PROJECT_ID> [REGION]"
  exit 1
fi

echo "🚀 Deploying NEXOVA to Google Cloud Platform..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# 1. Enable Required APIs for Build
echo "📦 Enabling APIs..."
gcloud services enable \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project $PROJECT_ID

# 2. Build and Push Images using Cloud Build
echo "🏗️ Building Backend Image..."
gcloud builds submit ../backend \
  --tag gcr.io/$PROJECT_ID/nexova-api:latest \
  --project $PROJECT_ID

echo "🏗️ Building Frontend Image..."
gcloud builds submit ../frontend \
  --tag gcr.io/$PROJECT_ID/nexova-web:latest \
  --project $PROJECT_ID

# 3. Apply Terraform
echo "☁️ Applying Terraform Infrastructure..."
cd terraform
terraform init
terraform apply -auto-approve -var="project_id=$PROJECT_ID" -var="region=$REGION"

echo "✅ Deployment Complete!"
echo "Backend URL: $(terraform output -raw backend_url)"
echo "Frontend URL: $(terraform output -raw frontend_url)"
