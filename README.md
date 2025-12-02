🌤️ CloudMart
Serverless E-Commerce API with FastAPI · Cosmos DB · Docker · GitHub Actions · Azure Container Instances

CloudMart is a lightweight cloud-native e-commerce platform built using FastAPI, Azure Cosmos DB, Docker, and GitHub Actions.
It demonstrates a full real-world cloud workflow:

Backend API with FastAPI

Live NoSQL database via Cosmos DB

Docker containerization

CI/CD automation

Deployment to Azure Container Instances (ACI)

🚀 Features
🛒 Core E-Commerce Functionality

Browse products

Filter by category

Manage a shopping cart

Place orders

Real-time database storage in Azure Cosmos DB

⚙️ Backend

FastAPI + Uvicorn application

Clean REST endpoints under /api/v1/*

Async Cosmos DB Python SDK

Fully Dockerized API service

☁️ Cloud Architecture

Azure Cosmos DB NoSQL

Docker Hub container image hosting

GitHub Actions CI/CD pipeline

Automated deploy to Azure Container Instances

Public DNS endpoint (ACI FQDN)

🧱 Tech Stack
Category	Technologies
Backend	FastAPI, Python 3.11
Database	Azure Cosmos DB (Core API)
Containerization	Docker, Azure Container Instances
CI/CD	GitHub Actions
Cloud	Azure Portal, ACI, VNet, NSG
Frontend	Vanilla JS, HTML5, CSS3
✅ Project Architecture Overview
          ┌──────────────────────────┐
          │      GitHub Repo         │
          └─────────────▲────────────┘
                        │ Push
                        │
          ┌─────────────▼────────────┐
          │    GitHub Actions CI/CD  │
          │  - Build Docker image    │
          │  - Push to Docker Hub    │
          │  - Deploy to Azure       │
          └─────────────▲────────────┘
                        │ Pull Image
                        │
        ┌───────────────▼────────────────┐
        │ Azure Container Instance (ACI) │
        │ cloudmart-app container        │
        └───────────────▲────────────────┘
                        │
                        │
          ┌─────────────▼────────────┐
          │     Cosmos DB (NoSQL)    │
          │ Products • Cart • Orders │
          └──────────────────────────┘

🧪 API Endpoints
Products
GET  /api/v1/products
GET  /api/v1/products?category=Electronics
GET  /api/v1/products/{id}

Cart
GET    /api/v1/cart
POST   /api/v1/cart/items
DELETE /api/v1/cart/items/{product_id}

Orders
POST /api/v1/orders
GET  /api/v1/orders

Health Check
GET /health

🐳 Docker
Build image
docker build -t cloudmart-api:local .

Run container locally
docker run -p 8000:80 \
  -e COSMOS_ENDPOINT="your-endpoint" \
  -e COSMOS_KEY="your-key" \
  cloudmart-api:local

🤖 CI/CD Pipeline

GitHub Actions automate:

🔨 Build Docker image

📦 Push image to Docker Hub

☁️ Deploy to Azure Container Instances

🧪 Health check validation

Workflows:

.github/workflows/ci.yml
.github/workflows/deploy.yml

🌐 Live Deployment

Public Endpoint:
(Example — replace with your actual)

http://cloudmart-1903054.canadacentral.azurecontainer.io/