# Utilise l'image de base appropriée
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt
COPY /requirements.txt /app/requirements.txt

# Installe le client MySQL et les dépendances Python
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'API
COPY . /app

# Commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
