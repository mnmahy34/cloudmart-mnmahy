# CPS451 Final Project: Enterprise Cloud Solution

## Complete Submission Documentation

### Student Information

Student ID: 138145230

Name: Mahdy Nesar Mahy

Course: CPS451NIA

Institution: Seneca College

Submission Date: 2nd December 2025

---

### Live Application URL

http://cloudmart-1903054.canadacentral.azurecontainer.io/

---

### Table of Contents

Project Overview

Azure Infrastructure Setup

Cosmos DB Configuration

Application Code

Docker Configuration

GitHub Actions CI/CD

Deployment Execution

API Testing & Verification

Browser Testing

CI/CD Verification

Complete Command Log

Project Summary

---

## 1. Project Overview

### CloudMart E-Commerce Platform

CloudMart is a serverless, containerized e-commerce platform built with:

FastAPI backend

Cosmos DB NoSQL database

Docker containerization

GitHub Actions CI/CD

Azure Container Instances (ACI)

Public DNS hosting

Automated deployment workflow

This project demonstrates enterprise-grade cloud architecture concepts including container hosting, network security, API-first design, NoSQL data storage, and automated deployments.

### Feature Summary

Feature | Implementation
--- | ---
Architecture | Multi-tier (Frontend + Backend API + DB)
Compute Platform | Azure Container Instances (ACI)
Database | Azure Cosmos DB (NoSQL)
CI/CD | GitHub Actions → Docker Hub → Azure ACI
Frontend | HTML/CSS/JS Static
Backend | FastAPI (Python 3.11)

---

## 2. Azure Infrastructure Setup

### Resources Created

Resource | Name
--- | ---
Resource Group | Student-RG-1903054
Cosmos DB Account | cloudmart-db-1903054
Cosmos Database | cloudmartdb
Containers | products, cart, orders
ACI Container Instance | cloudmart-app
DNS Label | cloudmart-1903054
Public URL | http://cloudmart-1903054.canadacentral.azurecontainer.io/
NSG | cloudmart-web-nsg

## 3. Cosmos DB Configuration

Database: cloudmartdb

Containers:

products

cart

orders

Each container uses **/id** as partition key.


---

## 4. Application Code

Backend built with FastAPI + Uvicorn, following clean REST patterns under `/api/v1/*`.

Key endpoints include:

GET /api/v1/products

GET /api/v1/products?category=Electronics

POST /api/v1/cart

GET /api/v1/cart

POST /api/v1/orders

GET /health

---

## 5. Docker Configuration

### Dockerfile (Backend)

```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Docker Hub Repository

https://hub.docker.com/repository/docker/mnmahy34/cloudmart-api/general

---

## 6. GitHub Actions CI/CD

https://github.com/mnmahy34/cloudmart-mnmahy

### Workflows included:

Workflow | Path
--- | ---
CI Workflow | .github/workflows/ci.yml
Deploy Workflow | .github/workflows/deploy.yml

### CI Workflow Summary

Checkout

Install Python

Install dependencies

Lint/test (optional)

Build Docker image (no push)

### Deploy Workflow Summary

Build Docker image

Login to Docker Hub

Push to Docker Hub

Login to Azure

Delete old ACI container

Deploy new one

Inject Cosmos DB secrets

Validate health endpoint

---

## 7. Deployment Execution

### Azure CLI Deployment Script (Used in Workflow)

```
az container create \
  --name cloudmart-app \
  --resource-group Student-RG-1903054 \
  --image mnmahy34/cloudmart-api:latest \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 80 \
  --dns-name-label cloudmart-1903054 \
  --environment-variables \
      COSMOS_ENDPOINT="https://cloudmart-db-1903054.documents.azure.com:443/" \
      COSMOS_KEY="$COSMOS_KEY"
```

## 8. API Testing & Verification

### Health Check
```
GET /health
```
Expected output:
```
{ "status": "ok" }
```


## 9. Browser Testing

Homepage with products listed

Category filter (e.g., Electronics)

Shopping cart with items

Order confirmation

Homepage

Category Filter

Shopping Cart

Order Confirmation

---

## 10. CI/CD Verification

Must show:

Image pushed to Docker Hub

ACI container recreated automatically

GitHub Actions logs clean

---

## 11. Complete Command Log

az cosmosdb create \
  --name cloudmart-db-1903054 \
  --resource-group Student-RG-1903054 \
  --kind GlobalDocumentDB \
  --locations regionName=canadacentral failoverPriority=0 \
  --default-consistency-level Eventual


az cosmosdb sql database create \
  --account-name cloudmart-db-1903054 \
  --resource-group Student-RG-1903054 \
  --name cloudmart

az cosmosdb sql container create \
  --account-name cloudmart-db-1903054 \
  --resource-group Student-RG-1903054 \
  --database-name cloudmart \
  --name products \
  --partition-key-path "/category"

az cosmosdb sql container create \
  --account-name cloudmart-db-1903054 \
  --resource-group Student-RG-1903054 \
  --database-name cloudmart \
  --name cart \
  --partition-key-path "/user_id"

az cosmosdb sql container create \
  --account-name cloudmart-db-1903054 \
  --resource-group Student-RG-1903054 \
  --database-name cloudmart \
  --name orders \
  --partition-key-path "/user_id"

az network nsg create \
  --resource-group Student-RG-1903054 \
  --name cloudmart-web-nsg \
  --location canadacentral



az network nsg rule create \
  --resource-group Student-RG-1903054 \
  --nsg-name cloudmart-web-nsg \
  --name Allow-HTTP \
  --priority 100 \
  --protocol Tcp \
  --direction Inbound \
  --access Allow \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-port-ranges 80

az network nsg rule create \
  --resource-group Student-RG-1903054 \
  --nsg-name cloudmart-web-nsg \
  --name Allow-HTTPS \
  --priority 110 \
  --protocol Tcp \
  --direction Inbound \
  --access Allow \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-port-ranges 443

az network nsg rule create \
  --resource-group Student-RG-1903054 \
  --nsg-name cloudmart-web-nsg \
  --name Allow-SSH \
  --priority 120 \
  --protocol Tcp \
  --direction Inbound \
  --access Allow \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-port-ranges 22


az container create \
  --name cloudmart-app \
  --resource-group Student-RG-1903054 \
  --image mnmahy34/cloudmart-api:latest \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 80 \
  --dns-name-label cloudmart-1903054 \
  --environment-variables \
    COSMOS_ENDPOINT="My_CosmosDB_EndPoint" \
    COSMOS_KEY="My_CosmosDB_Key"

---

## 12. Project Summary

CloudMart successfully demonstrates a real-world cloud-native e-commerce system:

API-first backend using FastAPI

Serverless NoSQL database using Cosmos DB

Fully dockerized application

Automated pipeline using GitHub Actions

Public deployment on Azure ACI

Docker Hub as container registry

Secure, stateless, high-availability architecture

This project meets the full requirements for Milestone 3 and showcases modern enterprise cloud engineering principles.

