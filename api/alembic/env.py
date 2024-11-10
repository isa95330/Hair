import sys
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# Ajouter le dossier 'api' au sys.path pour permettre l'importation de models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

# Importer correctement 'Base' depuis 'models.py' dans le dossier 'api'
from models import Base  # Importation de Base depuis 'api/models.py'

# Connexion à la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")

# Configuration d'Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Définir la cible des métadonnées (les tables à migrer)
target_metadata = Base.metadata

# Fonction pour exécuter les migrations en ligne
def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section),
                                     prefix='sqlalchemy.',
                                     poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Exécution des migrations selon le mode (en ligne ou hors ligne)
if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata)
    context.run_migrations()
else:
    run_migrations_online()
