import pytest
from fastapi.testclient import TestClient
from main import app
# Définir la fixture client pour le test
@pytest.fixture
def client():
    return TestClient(app)

# Test pour créer un produit
def test_create_product(client):
    # Créer une catégorie pour le produit
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Créer un produit
    file_path = "test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(b"fake image data")

    with open(file_path, "rb") as image_file:
        response = client.post(
            "/products/",
            files={"image": (file_path, image_file, "image/jpeg")},
            data={
                "name": "Test Product",
                "description": "Description of test product",
                "price": "99.99",  # Les valeurs numériques doivent être envoyées sous forme de chaînes dans multipart/form-data
                "category_id": str(category["id"])  # Assurez-vous que les nombres sont envoyés en tant que chaînes
            }
        )

        # Afficher le contenu de la réponse pour debug
        print(response.json())

    assert response.status_code == 200


def test_update_product(client):
    # Créer une catégorie pour le produit
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Créer un produit
    file_path = "test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(b"fake image data")

    with open(file_path, "rb") as image_file:
        response = client.post(
            "/products/",
            files={"image": (file_path, image_file, "image/jpeg")},
            data={
                "name": "Test Product",
                "description": "Description of test product",
                "price": "99.99",
                "category_id": str(category["id"])
            }
        )

    assert response.status_code == 200






def test_delete_product(client):

    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Créer un produit
    file_path = "test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(b"fake image data")

    with open(file_path, "rb") as image_file:
        response = client.post(
            "/products/",
            files={"image": (file_path, image_file, "image/jpeg")},
            data={
                "name": "Test Product",
                "description": "Description of test product",
                "price": "99.99",
                "category_id": str(category["id"])
            }
        )

    assert response.status_code == 200
    product = response.json()

    # Supprimer le produit
    response = client.delete(f"/products/{product['id']}")
    assert response.status_code == 200
    deleted_product = response.json()

    # Vérifier que le produit a été supprimé
    assert deleted_product["id"] == product["id"]
    assert deleted_product["name"] == product["name"]
    assert deleted_product["description"] == product["description"]
    assert deleted_product["price"] == product["price"]
    assert deleted_product["category_id"] == product["category_id"]
    assert deleted_product["image"] == product["image"]

def test_create_category(client):
    # Créer une catégorie
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Vérifier les données de la catégorie
    assert category["name"] == "Test Category"
    assert category["description"] == "Description of test category"
    assert "id" in category  # Vérifier que l'ID est renvoyé

def test_read_category(client):
    # Créer une catégorie
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Lire la catégorie créée
    response = client.get(f"/categories/{category['id']}")
    assert response.status_code == 200
    category_data = response.json()

    # Vérifier les données de la catégorie lue
    assert category_data["name"] == "Test Category"
    assert category_data["description"] == "Description of test category"
    assert category_data["id"] == category["id"]

def test_update_category(client):
    # Créer une catégorie
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response

def test_delete_category(client):
    # Créer une catégorie
    response = client.post("/categories/", json={"name": "Test Category", "description": "Description of test category"})
    assert response.status_code == 200
    category = response.json()

    # Supprimer la catégorie
    response = client.delete(f"/categories/{category['id']}")
    assert response.status_code == 200
    deleted_category = response.json()

    # Vérifier que la catégorie a été supprimée
    assert deleted_category["id"] == category["id"]
    assert deleted_category["name"] == category["name"]
    assert deleted_category["description"] == category["description"]
