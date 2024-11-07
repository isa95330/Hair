import os
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Form, UploadFile, File, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles
from models import Category, Product, get_db, ProductUpdate, Order, Shipping
from schemas import CategoryCreate, CategoryResponse, ProductResponse, UserResponse, UserCreate, \
    ShippingResponse, ShippingCreate  # Assurez-vous que ces schémas existent
from auth import create_user, login_user, verify_token, users_collection, admin_required
import aiofiles  # Importer aiofiles pour la gestion asynchrone des fichiers
import stripe

app = FastAPI()  # Crée une instance FastAPI
router = APIRouter()

# Configuration de CORS
origins = [
    "http://localhost:3000",  # URL de votre application frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
stripe.api_key = "sk_test_51NnUrjE0kqk9yRqfjgRvzIZLQR81us4UKRzV7RbQfhGRsEE0odCi2h4rO7unffFxaHtz2RlBuLAZ80mJFhjlrDGu003sMk32pI"

# Endpoint pour créer un Payment Intent
@app.post("/create-payment-intent/")
async def create_payment_intent(amount: float):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Amount in cents
            currency='eur'  # Your currency
        )
        return {"client_secret": payment_intent['client_secret']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# Route pour créer un utilisateur
@app.post("/users/", response_model=UserResponse)
async def register_user(user: UserCreate):
    return await create_user(user)

# Route pour se connecter et obtenir un JWT
@app.post("/login/")
async def login(email: str = Body(...), password: str = Body(...)):
    return await login_user(email, password)

# CRUD pour les catégories
@app.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter_by(id=category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter_by(id=category_id).first()

    if category_db is None:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.dict().items():
        setattr(category_db, key, value)

    db.commit()
    db.refresh(category_db)
    return category_db

@app.delete("/categories/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter_by(id=category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return category

# Spécifiez où seront sauvegardées les images
UPLOAD_DIRECTORY = "uploads"

# Montez le dossier uploads pour qu'il soit accessible depuis le navigateur
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

@app.post("/products/", response_model=ProductResponse)
async def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        category_id: int = Form(...),
        image: UploadFile = File(...)
):
    # Vérifiez si le répertoire d'uploads existe, sinon le créez
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    # Sauvegardez l'image dans le répertoire uploads de manière asynchrone
    file_location = f"{UPLOAD_DIRECTORY}/{image.filename}"
    async with aiofiles.open(file_location, "wb") as file:
        content = await image.read()
        await file.write(content)

    # Créez un nouveau produit dans la base de données avec le chemin de l'image
    db_product = Product(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        image=f"/uploads/{image.filename}"  # Chemin relatif pour l'image
    )
    db = next(get_db())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products



@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product

# main.py
@app.get("/admin/dashboard", dependencies=[Depends(admin_required)])
async def admin_dashboard():
    return {"message": "Welcome to the admin dashboard"}

# Exemple de route protégée par JWT
@app.get("/profile/", response_model=UserResponse)
async def get_profile(token: str = Depends(verify_token)):
    user = await users_collection.find_one({"email": token})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=str(user["_id"]),
        first_name=user["first_name"],
        last_name=user["last_name"],
        email=user["email"],
        is_admin=user.get("is_admin", False)  # Inclure le champ is_admin
    )
# Endpoint pour créer une commande
@app.post("/orders/")
async def create_order(user_id: str, total_amount: float, db: Session = Depends(get_db)):
    # Vérifiez si l'utilisateur existe dans MongoDB
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found in MongoDB")

    # Créez une nouvelle commande dans MySQL
    order = Order(user_id=user_id, total_amount=total_amount)
    db.add(order)
    db.commit()
    db.refresh(order)

    return {"order_id": order.id, "total_amount": order.total_amount}


# Endpoint pour récupérer les commandes d'un utilisateur
@app.get("/orders/{user_id}")
async def get_orders(user_id: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == str(user_id)).all()
    return orders

@app.post("/shippings/", response_model=ShippingResponse)
async def create_shipping(shipping: ShippingCreate, db: Session = Depends(get_db)):
    # Créez une nouvelle entrée de livraison dans la base de données
    db_shipping = Shipping(**shipping.dict())
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

@app.get("/shippings/{user_id}", response_model=List[ShippingResponse])
async def get_shippings(user_id: str, db: Session = Depends(get_db)):
    # Récupérez les informations de livraison pour un utilisateur donné
    shippings = db.query(Shipping).filter(Shipping.user_id == user_id).all()
    return shippings
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
