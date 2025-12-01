from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="CloudMart API", version="0.1.0")

# temporary data (in-memory)
PRODUCTS = [
    {"id": "1", "name": "Test Product", "category": "Electronics", "price": 9.99},
]

HTML_PAGE = """
<!DOCTYPE html>
<html>
  <head><title>CloudMart</title></head>
  <body>
    <h1>CloudMart</h1>
    <p>This is a placeholder frontend.</p>
  </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/health")
def health():
    return {"status": "healthy", "db_status": "disconnected"}

@app.get("/api/v1/products")
def list_products():
    return PRODUCTS