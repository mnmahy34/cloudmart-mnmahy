FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the deploy folder (your API lives here)
COPY deploy/ /app/

# Expose port for Azure
EXPOSE 80

# Run FastAPI
CMD ["uvicorn", "main_cosmosdb:app", "--host", "0.0.0.0", "--port", "80"]