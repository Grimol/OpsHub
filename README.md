# Activer venv
.venv/Scripts/activate

# Lancer API
uvicorn app.main:app --reload

# Lancer Docker
- Démarrer l'application Docker Desktop
docker compose up --build

# Migrations
alembic revision --autogenerate -m "msg"
alembic upgrade head

# Tests
pytest
