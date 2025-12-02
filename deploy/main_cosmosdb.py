from azure.cosmos import CosmosClient, exceptions
import os

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT", "")
COSMOS_KEY = os.environ.get("COSMOS_KEY", "")
DATABASE_NAME = "cloudmart"

client = None
database = None
products_container = None
cart_container = None
orders_container = None

def init_cosmos():
    global client, database, products_container, cart_container, orders_container

    if COSMOS_ENDPOINT and COSMOS_KEY:
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

        # Get database
        database = client.get_database_client(DATABASE_NAME)

        # Get containers
        products_container = database.get_container_client("products")
        cart_container = database.get_container_client("cart")
        orders_container = database.get_container_client("orders")


from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(title="CloudMart API", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    init_cosmos()
    print("==== STARTUP RUNNING ====")
    print("COSMOS_ENDPOINT:", COSMOS_ENDPOINT)
    print("COSMOS_KEY length:", len(COSMOS_KEY))
    print("products_container:", products_container)


# --------------------------------------------------
# In-memory data (NO database yet)
# --------------------------------------------------

PRODUCTS = [
    {"id": "1", "name": "Headphones", "category": "Electronics", "price": 99.99},
    {"id": "2", "name": "Shoes", "category": "Sports", "price": 59.99},
    {"id": "3", "name": "Keyboard", "category": "Electronics", "price": 29.99},
]

DEFAULT_USER = "demo"

CART = []
ORDERS = []

# --------------------------------------------------
# Models
# --------------------------------------------------

class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

# --------------------------------------------------
# Frontend homepage
# --------------------------------------------------

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>CloudMart</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .product { 
            border: 1px solid #ccc; 
            padding: 10px; 
            margin: 10px;
            display: inline-block;
            width: 200px;
        }
        .btn { 
            background: #007bff; 
            color: white; 
            padding: 8px; 
            border: none;
            cursor: pointer;
        }
        #cart { margin-top: 20px; padding: 10px; border: 1px solid #999; display:none; }
    </style>
</head>
<body>

    <h1>CloudMart</h1>

    <h2>Products</h2>
    <div id="products"></div>

    <button class="btn" onclick="toggleCart()">Show Cart</button>

    <div id="cart"></div>

    <script>
        async function loadProducts() {
            const res = await fetch('/api/v1/products');
            const data = await res.json();

            const container = document.getElementById('products');
            container.innerHTML = "";

            data.forEach(p => {
                container.innerHTML += `
                    <div class="product">
                        <h3>${p.name}</h3>
                        <p>Category: ${p.category}</p>
                        <p>Price: $${p.price}</p>
                        <button class="btn" onclick="addToCart('${p.id}')">Add to Cart</button>
                    </div>
                `;
            });
        }

        async function addToCart(id) {
            await fetch('/api/v1/cart/items', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: id, quantity: 1})
            });
            alert("Added to cart");
        }

        async function loadCart() {
            const res = await fetch('/api/v1/cart');
            const data = await res.json();

            const cartDiv = document.getElementById('cart');
            cartDiv.innerHTML = "<h2>Your Cart</h2>";

            data.forEach(item => {
                cartDiv.innerHTML += `
                    <p>Product: ${item.product_id} — Qty: ${item.quantity}
                    <button onclick="removeItem('${item.product_id}')">Remove</button></p>
                `;
            });

            cartDiv.innerHTML += `<button class="btn" onclick="placeOrder()">Place Order</button>`;
        }

        async function removeItem(id) {
            await fetch('/api/v1/cart/items/' + id, { method: 'DELETE' });
            loadCart();
        }

        async function placeOrder() {
            const res = await fetch('/api/v1/orders', { method: 'POST' });
            const data = await res.json();
            alert("Order placed: " + data.id);
            loadCart();
        }

        function toggleCart() {
            const cartDiv = document.getElementById('cart');
            if (cartDiv.style.display === "none") {
                cartDiv.style.display = "block";
                loadCart();
            } else {
                cartDiv.style.display = "none";
            }
        }

        loadProducts();
    </script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():
    try:
        await cosmos_container.read_item(item="1", partition_key="1")
        return {"status": "healthy", "db": "connected"}
    except Exception as e:
        return {"status": "healthy", "db": "not_connected_yet"}

# --------------------------------------------------
# Product endpoints
# --------------------------------------------------

@app.get("/api/v1/products")
def list_products(category: str | None = None):
    if not products_container:
        return []  # fallback if Cosmos not ready

    if category:
        query = "SELECT * FROM c WHERE c.category = @category"
        params = [{"name": "@category", "value": category}]
        items = products_container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        )
    else:
        items = products_container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )

    return list(items)

@app.get("/api/v1/products/{product_id}")
def get_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/v1/categories")
def list_categories():
    return sorted({p["category"] for p in PRODUCTS})

# --------------------------------------------------
# Cart endpoints
# --------------------------------------------------

@app.get("/api/v1/cart")
def get_cart():
    if not cart_container:
        return []

    query = "SELECT * FROM c WHERE c.user_id = @u"
    params = [{"name": "@u", "value": DEFAULT_USER}]
    items = cart_container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    )
    return list(items)


@app.post("/api/v1/cart/items")
def add_cart_item(item: CartItem):

    # Check if product already in cart
    query = "SELECT * FROM c WHERE c.user_id=@u AND c.product_id=@p"
    params = [
        {"name": "@u", "value": DEFAULT_USER},
        {"name": "@p", "value": item.product_id}
    ]

    existing_items = list(cart_container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    if existing_items:
        doc = existing_items[0]
        doc["quantity"] = item.quantity
        cart_container.upsert_item(doc)
        return {"message": "Updated quantity"}

    # Create new cart item
    new_item = {
        "id": str(uuid.uuid4()),
        "user_id": DEFAULT_USER,
        "product_id": item.product_id,
        "quantity": item.quantity,
    }
    cart_container.create_item(new_item)
    return {"message": "Added to cart"}


@app.delete("/api/v1/cart/items/{product_id}")
def remove_cart_item(product_id: str):

    # Find items
    query = "SELECT * FROM c WHERE c.user_id=@u AND c.product_id=@p"
    params = [
        {"name": "@u", "value": DEFAULT_USER},
        {"name": "@p", "value": product_id},
    ]

    items = cart_container.query_items(
        query=query, parameters=params, enable_cross_partition_query=True
    )

    for doc in items:
        cart_container.delete_item(
            item=doc["id"],
            partition_key=doc["user_id"]
        )

    return {"message": "Removed from cart"}


# --------------------------------------------------
# Orders endpoints
# --------------------------------------------------

@app.post("/api/v1/orders")
def create_order():
    # Get user cart
    query = "SELECT * FROM c WHERE c.user_id=@u"
    params = [{"name": "@u", "value": DEFAULT_USER}]
    cart_items = list(cart_container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_doc = {
        "id": str(uuid.uuid4()),
        "user_id": DEFAULT_USER,
        "items": [
            {"product_id": c["product_id"], "quantity": c["quantity"]}
            for c in cart_items
        ],
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat()
    }

    orders_container.create_item(order_doc)

    # Clear cart
    for doc in cart_items:
        cart_container.delete_item(doc["id"], doc["user_id"])

    return order_doc


@app.get("/api/v1/orders")
def list_orders():
    return [o for o in ORDERS if o["user_id"] == DEFAULT_USER]