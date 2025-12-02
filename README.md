# 🌩️ CloudMart --- Serverless E-Commerce API & UI

**FastAPI + Azure Cosmos DB + Docker + GitHub Actions CI/CD + Azure
Container Instances**

<p align="center"> <img src="https://img.shields.io/github/actions/workflow/status/mnmahy34/cloudmart-mnmahy/ci.yml?label=CI%20Build&logo=github&style=flat-square" /> <img src="https://img.shields.io/github/actions/workflow/status/mnmahy34/cloudmart-mnmahy/deploy.yml?label=Deploy%20to%20Azure&logo=azure-pipelines&style=flat-square" /> <img src="https://img.shields.io/docker/pulls/mnmahy34/cloudmart-api?logo=docker&style=flat-square" /> <img src="https://img.shields.io/github/license/mnmahy34/cloudmart-mnmahy?style=flat-square" /> </p>

CloudMart is a lightweight real-world cloud architecture demo: a fully
dockerized FastAPI backend + CosmosDB NoSQL database + vanilla JS
frontend deployed through GitHub Actions to Azure Container Instances
(ACI). It demonstrates real production concepts: API design, CI/CD
automation, container hosting, NSGs, VNet, Docker Hub publishing, and
cloud-native app structure.

------------------------------------------------------------------------

## 🚀 Core Features

### 🛒 E-Commerce Functionality

-   Browse products\
-   Filter by category\
-   Add items to cart\
-   View cart\
-   Place orders\
-   Order confirmation screen\
-   Live data stored in Azure Cosmos DB

### ⚙️ Backend Tech

-   FastAPI + Uvicorn\
-   Clean REST endpoints under `/api/v1/*`\
-   Async Cosmos DB Python SDK\
-   Dockerized backend service (Dockerfile)

### ☁️ Cloud Architecture

-   Azure Cosmos DB (NoSQL)\
-   Azure Container Instances (ACI)\
-   Azure Network Security Group (NSG)\
-   VNet Integration\
-   Custom DNS label on Azure\
-   GitHub Actions CI/CD automation\
-   Docker Hub image hosting

------------------------------------------------------------------------

## 🧱 Project Architecture Overview

    GitHub Repo
       │
       ├── CI Workflow (ci.yml)
       │      ├── Install Python deps
       │      ├── Lint / test (optional)
       │      └── Build docker image (no push)
       │
       ├── Deploy Workflow (deploy.yml)
       │      ├── Build Docker image
       │      ├── Push to Docker Hub ➜ mnmahy34/cloudmart-api:latest
       │      ├── Login to Azure
       │      ├── Delete old ACI instance
       │      └── Create new ACI instance with env vars
       │
       ▼

    Docker Hub Registry
       └── cloudmart-api:latest
           (public container image)
       ▼

    Azure Container Instances (ACI)
       ├── Pull new Docker image
       ├── Expose port 80
       ├── Inject Cosmos DB secrets
       └── Public DNS → cloudmart-<id>.canadacentral.azurecontainer.io
       ▼

    Azure Cosmos DB (NoSQL)
       ├── products
       ├── cart
       └── orders

------------------------------------------------------------------------

## 📦 Docker Hub Repository

📍 **https://hub.docker.com/r/mnmahy34/cloudmart-api**

Tags: - `latest` (auto-deployed through GitHub Actions)

------------------------------------------------------------------------

## 🧪 GitHub Actions CI/CD Workflows

### 📄 `.github/workflows/ci.yml`

Runs on every push to **main** or PR: - Checkout repo\
- Install dependencies\
- Optional lint/testing\
- Docker build test

### 📄 `.github/workflows/deploy.yml`

Runs on every push to **main**: - Build and push Docker image\
- Login with Azure Service Principal\
- Recreate container instance on Azure\
- Run health check

------------------------------------------------------------------------

## 🔐 GitHub Secrets Required

  Secret Name          Purpose
  -------------------- --------------------------------
  DOCKERHUB_USERNAME   Docker Hub login
  DOCKERHUB_TOKEN      Docker Hub access token
  AZURE_CREDENTIALS    Azure service principal (JSON)
  COSMOS_ENDPOINT      Cosmos DB endpoint URL
  COSMOS_KEY           Cosmos DB primary key
  USER_ID              Student/lab identifier

------------------------------------------------------------------------

## ▶️ Running Locally

### 1. Build the Docker image

``` bash
docker build -t cloudmart-api:local .
```

### 2. Run locally

``` bash
docker run -p 8000:80 \
  -e COSMOS_ENDPOINT="your-endpoint" \
  -e COSMOS_KEY="your-key" \
  cloudmart-api:local
```

Open:

👉 http://localhost:8000/health\
👉 http://localhost:8000

------------------------------------------------------------------------

## 🌐 Production Deployment URL

**http://cloudmart-1903054.canadacentral.azurecontainer.io/**
