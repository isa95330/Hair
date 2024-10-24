import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from main import app

# Configuration du client de test pour FastAPI
@pytest.fixture(scope="module")  # Utilise le même client pour tous les tests dans le module
def client():
    # Connexion à une base de données MongoDB temporaire pour les tests
    app.mongodb_client = AsyncIOMotorClient("mongodb://mongo:27017")
    app.mongodb = app.mongodb_client["test_userdatabase"]  # Base de données de test

    with TestClient(app) as client:
        yield client

    # Nettoyage après tous les tests
    app.mongodb["users"].drop()
    app.mongodb_client.close()  # Fermer la connexion MongoDB

# Test de création d'utilisateur
def test_create_user(client: TestClient):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Test St",
        "phone_number": "1234567890",
        "email": "john.doe@example.com",
        "password": "password123"
    }

    # Envoi de la requête pour créer un utilisateur
    response = client.post("/users/", json=user_data)
    print(response.json())  # Imprimez la réponse pour déboguer

    assert response.status_code == 200  # Vérifiez que l'utilisateur est bien créé
    user = response.json()

    # Vérifications des données de l'utilisateur
    assert user["first_name"] == "John"
    assert user["last_name"] == "Doe"
    assert user["address"] == "123 Test St"
    assert user["phone_number"] == "1234567890"
    assert user["email"] == "john.doe@example.com"
    assert "id" in user  # Assurez-vous que l'ID est renvoyé


def test_login(client: TestClient):
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }

    response = client.post("/login", json=login_data)
    print(response.json())  # Affichez le contenu de la réponse

    assert response.status_code == 400
