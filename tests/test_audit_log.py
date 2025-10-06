from fastapi.testclient import TestClient


def test_create_audit_log(client: TestClient, user_factory):
    user = user_factory()

    payload = {
        "action": "CREATE",
        "table_name": "users",
        "record_id": user.id,
        "user_id": user.id,
        "payload": {"field": "value"},
    }

    response = client.post("/api/v1/audit-logs", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["action"] == "CREATE"
    assert data["table_name"] == "users"
    assert data["record_id"] == user.id


def test_list_audit_logs(client: TestClient, audit_log_factory):
    # Créer quelques logs
    audit_log_factory(action="CREATE")
    audit_log_factory(action="UPDATE")

    response = client.get("/api/v1/audit-logs")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    # Les logs sont triés par date décroissante
    assert data[0]["action"] in ["CREATE", "UPDATE"]
    assert data[1]["action"] in ["CREATE", "UPDATE"]


def test_get_audit_log(client: TestClient, audit_log_factory):
    audit_log = audit_log_factory(action="DELETE")

    response = client.get(f"/api/v1/audit-logs/{audit_log.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["action"] == "DELETE"
    assert data["id"] == audit_log.id


def test_get_audit_log_not_found(client: TestClient):
    response = client.get("/api/v1/audit-logs/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Audit log not found"
