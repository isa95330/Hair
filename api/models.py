import os
from typing import Optional

from pydantic.v1 import EmailStr, BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, DECIMAL
from sqlalchemy.orm import relationship, sessionmaker
from pymysql import install_as_MySQLdb
install_as_MySQLdb()
from sqlalchemy.orm import declarative_base

DATABASE_USER = "isadev95"  # Utilisateur MySQL
DATABASE_PASSWORD = "domont"  # Mot de passe MySQL
DATABASE_HOST = "isadev95.mysql.pythonanywhere-services.com"  # Hôte MySQL
DATABASE_NAME = "hairdb"  # Nom de la base de données

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}"
print(DATABASE_URL)
Base = declarative_base()
engine = None  # Initialiser engine à None

try:
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Erreur de connexion à la base de données : {e}")

# Créer SessionLocal seulement si l'engine est défini
if engine is not None:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None  # Ou gérer cela d'une autre manière


# Fonction pour obtenir une session de base de données
def get_db():
    if SessionLocal is None:
        raise Exception("La connexion à la base de données n'est pas établie.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(250), index=True)
    # Relation vers Product
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(250), index=True)
    price = Column(Float, index=True)
    image = Column(String(250), index=True)

    category_id = Column(Integer, ForeignKey('categories.id'))

    # Relation vers Category
    category = relationship('Category', back_populates='products')

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    image: Optional[str] = None  # Optionnel pour permettre la mise à jour sans image

class Order(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))   # Utilisez un String pour l'ID utilisateur MongoDB
    total_amount = Column(DECIMAL(10, 2))



class Shipping(Base):
    __tablename__ = 'shippings'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))  # Assurez-vous que cela correspond à votre modèle d'utilisateur
    address = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)



print("models loaded successfully")
# Créez les tables
Base.metadata.create_all(bind=engine)