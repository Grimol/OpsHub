# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Evite les .pyc, force le flush stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Dossier de travail
WORKDIR /app

# Installer dépendances
COPY requirements*.txt /app/
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copier le code
COPY app /app/app

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
