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

import os

# Base de données temporaire pour les tests
import tempfile
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from app.db.models import (
    AuditLog,
    Project,
    ProjectStatus,
    Ticket,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
)
from app.main import app


@pytest.fixture(scope="session")
def engine():
    """Moteur de base de données temporaire pour tous les tests."""
    # Créer un fichier temporaire pour la session de tests
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)  # Fermer le descripteur de fichier

    test_db_url = f"sqlite:///{db_path}"

    eng = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        echo=False,  # Mettre à True pour voir les requêtes SQL
    )

    # Créer toutes les tables une seule fois pour la session
    Base.metadata.create_all(bind=eng)

    yield eng

    # Nettoyage : supprimer le fichier temporaire à la fin
    try:
        os.unlink(db_path)
    except (OSError, FileNotFoundError, PermissionError):
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

    def _create_user(email=None, full_name="Test User", role=UserRole.viewer):
        if email is None:
            email = f"user_{uuid.uuid4().hex[:8]}@example.com"

        user = User(email=email, full_name=full_name, role=role)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _create_user


@pytest.fixture
def project_factory(db_session):
    """Factory pour créer des projets de test."""

    def _create_project(**kwargs):
        defaults = {
            "name": "Test Project",
            "description": "Test description",
            "status": ProjectStatus.active,
        }
        defaults.update(kwargs)
        project = Project(**defaults)
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        return project

    return _create_project


@pytest.fixture
def ticket_factory(db_session, user_factory, project_factory):
    """Factory pour créer des tickets de test."""

    def _create_ticket(**kwargs):
        # Créer les dépendances si pas fournies
        if "project_id" not in kwargs:
            project = project_factory()
            kwargs["project_id"] = project.id

        if "assignee_id" not in kwargs:
            user = user_factory()
            kwargs["assignee_id"] = user.id

        defaults = {
            "title": "Test Ticket",
            "description": "Test description",
            "priority": TicketPriority.med,
            "status": TicketStatus.open,
        }
        defaults.update(kwargs)
        ticket = Ticket(**defaults)
        db_session.add(ticket)
        db_session.commit()
        db_session.refresh(ticket)
        return ticket

    return _create_ticket


@pytest.fixture
def audit_log_factory(db_session):
    """Factory pour créer des logs d'audit de test."""

    def _create_audit_log(**kwargs):
        defaults = {
            "action": "CREATE",
            "table_name": "test_table",
            "record_id": 1,
            "payload": {"test": "data"},
        }
        defaults.update(kwargs)
        audit_log = AuditLog(**defaults)
        db_session.add(audit_log)
        db_session.commit()
        db_session.refresh(audit_log)
        return audit_log

    return _create_audit_log
