from http import HTTPStatus

from app.db.enums import UserRole


def test_create_project_ok(client, auth_headers):
    headers, owner = auth_headers(role=UserRole.admin)

    payload = {
        "name": "Alpha",
        "description": "Premier projet",
        "status": "active",
        "owner_id": owner.id,
    }
    r = client.post("/projects", json=payload, headers=headers)
    assert r.status_code == HTTPStatus.CREATED, r.text

    body = r.json()
    assert body["name"] == "Alpha"
    assert body["description"] == "Premier projet"
    assert body["status"] == "active"
    assert body["owner_id"] == owner.id


def test_list_projects(client, auth_headers):
    headers, owner = auth_headers(role=UserRole.admin)

    payload1 = {
        "name": "Alpha",
        "description": "Premier projet",
        "status": "active",
        "owner_id": owner.id,
    }

    payload2 = {
        "name": "Beta",
        "description": "Second projet",
        "status": "active",
        "owner_id": owner.id,
    }

    client.post("/projects", json=payload1, headers=headers)
    client.post("/projects", json=payload2, headers=headers)

    r = client.get("/projects", headers=headers)
    print(r)
    assert r.status_code == HTTPStatus.OK
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    names = [p["name"] for p in data]
    assert "Alpha" in names and "Beta" in names


def test_get_project_ok(client, user_factory, project_factory):
    o = user_factory(email="owner3@example.com")
    r_create = project_factory(name="Solo", owner_id=o.id)
    pid = r_create.id

    r = client.get(f"/projects/{pid}")
    assert r.status_code == HTTPStatus.OK
    assert r.json()["name"] == "Solo"


def test_get_project_not_found(client):
    r = client.get("/projects/999999")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "Project not found"


def test_update_project_ok(client, user_factory, project_factory):
    o = user_factory(email="owner4@example.com")
    r_create = project_factory(name="Old", owner_id=o.id)
    pid = r_create.id

    payload = {"name": "New", "description": "Maj", "status": "archived"}
    r = client.put(f"/projects/{pid}", json=payload)
    assert r.status_code == HTTPStatus.OK, r.text
    body = r.json()
    assert body["name"] == "New"
    assert body["description"] == "Maj"
    assert body["status"] == "archived"


def test_update_project_not_found(client):
    r = client.put("/projects/424242", json={"name": "X"})
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "Project not found"


def test_delete_project_ok(client, user_factory, project_factory):
    o = user_factory(email="owner5@example.com")
    r_create = project_factory(name="Del", owner_id=o.id)
    pid = r_create.id

    r = client.delete(f"/projects/{pid}")
    assert r.status_code == HTTPStatus.NO_CONTENT

    r2 = client.get(f"/projects/{pid}")
    assert r2.status_code == HTTPStatus.NOT_FOUND


def test_delete_project_not_found(client):
    r = client.delete("/projects/111111")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "Project not found"
