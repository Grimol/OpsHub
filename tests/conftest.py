"""
conftest.py
------------
Configuration simplifiée pour les tests avec base de données en mémoire.

Objectifs :
- Base SQLite en mémoire (:memory:) - rapide et sans fichiers
- Création automatique des tables via SQLAlchemy metadata
- Session isolée par test avec nettoyage automatique
- Override de la dépendance FastAPI get_db
- Factory pour créer facilement des données de test
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_db
from app.db.base import Base
from app.db import models  # Important : importer pour que les modèles soient enregistrés


# Base de données temporaire pour les tests
import tempfile
import os

@pytest.fixture(scope="session")
def engine():
    """Moteur de base de données temporaire pour tous les tests."""
    # Créer un fichier temporaire pour la session de tests
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)  # Fermer le descripteur de fichier
    
    test_db_url = f"sqlite:///{db_path}"
    
    eng = create_engine(
        test_db_url, 
        connect_args={"check_same_thread": False},
        echo=False  # Mettre à True pour voir les requêtes SQL
    )
    
    # Créer toutes les tables une seule fois pour la session
    Base.metadata.create_all(bind=eng)
    
    yield eng
    
    # Nettoyage : supprimer le fichier temporaire à la fin
    try:
        os.unlink(db_path)
    except:
        pass


@pytest.fixture(scope="function") 
def db_session(engine):
    """
    Session de base de données pour le test.
    Pas besoin de nettoyage avec une base en mémoire !
    """
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Client HTTP de test avec override de la dépendance get_db.
    L'API utilisera automatiquement notre session de test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Remplacer la dépendance
    app.dependency_overrides[get_db] = override_get_db
    
    # Créer le client de test
    with TestClient(app) as test_client:
        yield test_client
    
    # Nettoyer les overrides
    app.dependency_overrides.clear()


@pytest.fixture
def user_factory(db_session):
    """
    Factory pour créer facilement des utilisateurs de test.
    
    Usage:
        user = user_factory()  # Utilisateur avec email aléatoire
        user = user_factory(email="test@example.com", full_name="Test User")
    """
    from app.db.models import User, UserRole
    
    def _create_user(email=None, full_name="Test User", role=UserRole.viewer):
        if email is None:
            email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        
        user = User(
            email=email,
            full_name=full_name,
            role=role
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    
    return _create_user