# tests/test_users.py
from http import HTTPStatus


def test_email_conflict(client, user_factory):
    # Arrange : j'ai déjà un user avec un email valide
    user_factory(email="dup@example.com")

    # Act : je tente de créer le même via l'API
    payload = {"email": "dup@example.com", "full_name": "Dup", "role": "viewer"}
    r = client.post("/users", json=payload)

    # Assert
    assert r.status_code == HTTPStatus.CONFLICT  # Maintenant on devrait avoir le bon code !
    assert r.json()["detail"] == "Email already exists"


def test_create_user_validation(client):
    r = client.post("/users", json={"email": "bad", "full_name": "X", "role": "viewer"})
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_user_ok(client, user_factory):
    u = user_factory(email="get1@example.com", full_name="Get One")
    r = client.get(f"/users/{u.id}")
    assert r.status_code == HTTPStatus.OK, r.text
    body = r.json()
    assert body["id"] == u.id
    assert body["email"] == "get1@example.com"
    assert body["full_name"] == "Get One"


def test_get_user_not_found(client):
    r = client.get("/users/999999")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "User not found"


def test_update_user_ok(client, user_factory):
    u = user_factory(email="upd1@example.com", full_name="Old Name")
    payload = {"full_name": "New Name", "role": "manager"}
    r = client.put(f"/users/{u.id}", json=payload)
    assert r.status_code == HTTPStatus.OK, r.text
    body = r.json()
    assert body["id"] == u.id
    assert body["full_name"] == "New Name"
    assert body["role"] == "manager"


def test_update_user_not_found(client):
    r = client.put("/users/424242", json={"full_name": "X"})
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "User not found"


def test_delete_user_ok(client, user_factory):
    u = user_factory(email="del1@example.com")
    r = client.delete(f"/users/{u.id}")
    assert r.status_code == HTTPStatus.NO_CONTENT, r.text
    # vérifier qu'il n'existe plus
    r2 = client.get(f"/users/{u.id}")
    assert r2.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_not_found(client):
    r = client.delete("/users/111111")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "User not found"
