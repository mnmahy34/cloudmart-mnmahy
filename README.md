🌥️ CloudMart — Serverless Shopping API

FastAPI • Azure Cosmos DB • Docker • Azure Container Instances • GitHub Actions CI/CD

CloudMart is a lightweight shopping API and frontend built with FastAPI, backed by Azure Cosmos DB, containerized with Docker, and deployed automatically to Azure Container Instances (ACI) using GitHub Actions.

This project was developed as part of a cloud-computing assignment to demonstrate:
✔ REST API design
✔ Cloud database use
✔ Containerization
✔ Deployment automation
✔ GitHub Actions pipelines

✨ Features
REST API Endpoints
Method	Endpoint	Description
GET	/	Frontend web page
GET	/health	Health check
GET	/api/v1/products	List all products
GET	/api/v1/products?category=	Filter products by category
GET	/api/v1/products/{id}	Get product details
GET	/api/v1/categories	List distinct product categories
GET	/api/v1/cart	Get current user's cart
POST	/api/v1/cart/items	Add/update cart item
DELETE	/api/v1/cart/items/{id}	Remove item from cart
POST	/api/v1/orders	Create an order
GET	/api/v1/orders	List user orders
🗄️ Database (Azure Cosmos DB)

Cosmos DB Account:
cloudmart-db-1903054

Database:
cloudmart

Containers:

Container	Partition Key
products	/category
cart	/user_id
orders	/user_id

Your FastAPI app loads data using:

from azure.cosmos import CosmosClient
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

🖥️ Frontend

A simple frontend UI is served directly from FastAPI as HTML + CSS + JavaScript:

✔ Displays product cards
✔ Filters by category
✔ Adds items to cart
✔ Shows cart modal
✔ Places orders

Accessible at:

http://localhost:8000/


or after deployment:

http://cloudmart-1903054.canadacentral.azurecontainer.io/

🐳 Docker Deployment
Build Docker image:
docker build -t cloudmart-api:local .

Run locally with Cosmos DB credentials:
docker run -p 8000:80 \
  -e COSMOS_ENDPOINT="https://cloudmart-db-1903054.documents.azure.com:443/" \
  -e COSMOS_KEY="<my_cosmosDB_key>" \
  cloudmart-api:local

🚀 Azure Deployment (ACI)
Push image to Docker Hub
docker tag cloudmart-api:local <mnmahy34>/cloudmart-api:latest
docker login
docker push <mnmahy34>/cloudmart-api:latest

Create Azure Container Instance
az container create \
  --name cloudmart-app \
  --resource-group Student-RG-1903054 \
  --image <mnmahy34>/cloudmart-api:latest \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 80 \
  --dns-name-label cloudmart-1903054 \
  --environment-variables \
    COSMOS_ENDPOINT="https://cloudmart-db-1903054.documents.azure.com:443/" \
    COSMOS_KEY="<my_cosmosDB_key>"


Check deployment:

az container show \
  --name cloudmart-app \
  --resource-group Student-RG-1903054 \
  --query '{state:instanceView.state, fqdn:ipAddress.fqdn}' -o table

🔄 CI/CD (GitHub Actions)

Configured with:

✔ ci.yml

Install Python dependencies

Run formatting / lint

Validate build

✔ deploy.yml

Build Docker image

Push to Docker Hub

Log into Azure

Delete old container (if exists)

Deploy new container with environment variables

Call /health endpoint to verify

Secrets required:
Secret Name	Purpose
DOCKERHUB_USERNAME	Docker Hub login
DOCKERHUB_TOKEN	Docker Hub PAT
AZURE_CREDENTIALS	Service Principal JSON (--sdk-auth)
COSMOS_ENDPOINT	Cosmos DB endpoint
COSMOS_KEY	Cosmos DB primary key