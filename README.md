🌥️ CloudMart – Serverless E-Commerce API with Cosmos DB + Docker + GitHub Actions + ACI

CloudMart is a lightweight e-commerce demo platform built with FastAPI, Azure Cosmos DB, and Docker.
The project demonstrates real-world cloud architecture: API backend, database integration, containers, CI/CD automation, and deployment to Azure Container Instances (ACI).

⭐ Features
🛒 API Functionality

View products

Manage cart

Place orders

Live data storage using Cosmos DB

⚙️ Backend

FastAPI + Uvicorn

Async Cosmos DB SDK

Clean endpoints under /api/v1/*

Dockerized backend service

☁️ Cloud Architecture

Cosmos DB NoSQL database

Docker Hub image hosting

GitHub Actions CI/CD

Automatic deploy to Azure Container Instances

Custom DNS label on Azure

📁 Project Structure
cloudmart/
│── deploy/
│   └── main_cosmosdb.py       # FastAPI backend
│
│── Dockerfile                 # Container build file
│── requirements.txt           # Python dependencies
│── README.md
│
└── .github/workflows/
    ├── ci.yml                 # CI: tests + checks
    └── deploy.yml             # CD: build + push + deploy

🐳 Docker Support
Build image locally:
docker build -t cloudmart-api:local .

Run locally:
docker run -p 8000:80 \
  -e COSMOS_ENDPOINT="your-endpoint" \
  -e COSMOS_KEY="your-key" \
  cloudmart-api:local


Backend reachable at:

http://localhost:8000

🧪 API Endpoints
Method	Endpoint	Description
GET	/api/v1/products	List all products
GET	/api/v1/cart	View cart
POST	/api/v1/cart/{id}	Add product to cart
POST	/api/v1/orders	Place order
GET	/health	Health check
🚀 CI/CD Overview
🔧 CI (ci.yml)

Runs automatically on push:

Checkout

Install Python

Lint / validate

(Optional) Build Docker image

💠 CD (deploy.yml)

Triggered on push to main:

Build Docker image

Log in to Docker Hub

Push latest tag

Log in to Azure

Delete old container

Recreate container with latest image

Health check

🔑 Required GitHub Secrets

Make sure these secrets exist:

Secret Name	Description
DOCKERHUB_USERNAME	Your Docker Hub username
DOCKERHUB_TOKEN	Docker Hub access token
AZURE_CREDENTIALS	Service principal JSON
AZURE_RESOURCE_GROUP	e.g. Student-RG-1903054
USER_ID	Your student ID for DNS label
COSMOS_ENDPOINT	Cosmos DB endpoint URL
COSMOS_KEY	Cosmos DB key
☁️ Azure Deployment (ACI)
After CI/CD completes, your app is reachable at:
http://cloudmart-<yourid>.canadaeast.azurecontainer.io


Health check:

http://cloudmart-<yourid>.canadaeast.azurecontainer.io/health

🎓 Purpose

This project was developed for Seneca College – OPS coursework, demonstrating:

Cloud infrastructure setup

Docker containerization

Cosmos DB NoSQL modeling

CI/CD pipelines (GitHub Actions → Docker Hub → Azure)

Real-world deployment workflows

❤️ Acknowledgements

Thanks to Azure, GitHub Actions, and FastAPI — the trio that brings modern cloud development to life.