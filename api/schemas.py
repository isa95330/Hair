from typing import Optional, List
from pydantic import BaseModel

# Schéma pour la création d'un utilisateur
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    address: str = None
    phone_number: str = None
    is_admin: bool = False  # Champ pour indiquer si c'est un admin



# Schéma pour la réponse utilisateur
class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    address: str  # Assurez-vous que ces champs sont là
    phone_number: str

    class Config:
        from_attributes = True



# Modèle de base pour les catégories
class CategoryBase(BaseModel):
    name: str
    description: str

# Modèle utilisé pour la création d'une catégorie (sans ID)
class CategoryCreate(CategoryBase):
    pass  # Rien à ajouter, tout est hérité de CategoryBase

# Modèle de réponse pour une catégorie, avec l'ID
class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # Remplacez orm_mode par from_attributes


# Modèle de base pour les produits
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int  # Relation avec la catégorie
    image: Optional[str]  # Rendre l'image optionnelle

    class Config:
        from_attributes = True  # Utiliser from_attributes au lieu de orm_mode

# Modèle utilisé pour la création d'un produit (sans ID)
class ProductCreate(ProductBase):
    pass

# Modèle de réponse pour un produit, avec l'ID
class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Remplacez orm_mode par from_attributes
print("Schemas loaded successfully")
