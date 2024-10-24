from typing import Optional

from pydantic.v1 import EmailStr, BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from pymysql import install_as_MySQLdb
install_as_MySQLdb()
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+pymysql://root:domont95@mysql_db:3306/hairdb"

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


print("models loaded successfully")
