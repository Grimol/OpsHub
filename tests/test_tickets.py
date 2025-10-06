from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.enums import TicketPriority, TicketStatus
from app.db.models import Ticket


def test_create_ticket(client: TestClient, user_factory, project_factory):
    # Créer les dépendances
    user = user_factory()
    project = project_factory(owner_id=user.id)

    payload = {
        "title": "Test Ticket",
        "description": "Test description",
        "priority": TicketPriority.high.value,
        "status": TicketStatus.open.value,
        "project_id": project.id,
        "assignee_id": user.id,
    }

    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["priority"] == TicketPriority.high.value
    assert data["project_id"] == project.id


def test_list_tickets(client: TestClient, ticket_factory):
    # Créer quelques tickets
    ticket_factory(title="Ticket 1")
    ticket_factory(title="Ticket 2")

    response = client.get("/api/v1/tickets")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Ticket 1"
    assert data[1]["title"] == "Ticket 2"


def test_get_ticket(client: TestClient, ticket_factory):
    ticket = ticket_factory(title="Test Ticket")

    response = client.get(f"/api/v1/tickets/{ticket.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["id"] == ticket.id


def test_get_ticket_not_found(client: TestClient):
    response = client.get("/api/v1/tickets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_update_ticket(client: TestClient, ticket_factory):
    ticket = ticket_factory(title="Original Title")

    payload = {
        "title": "Updated Title",
        "status": TicketStatus.done.value,
    }

    response = client.put(f"/api/v1/tickets/{ticket.id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == TicketStatus.done.value


def test_delete_ticket(client: TestClient, ticket_factory, db_session: Session):
    ticket = ticket_factory(title="To Delete")
    ticket_id = ticket.id

    response = client.delete(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 204

    # Vérifier que le ticket a été supprimé
    deleted_ticket = db_session.query(Ticket).filter(Ticket.id == ticket_id).first()
    assert deleted_ticket is None
