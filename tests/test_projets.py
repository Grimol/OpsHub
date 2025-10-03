from http import HTTPStatus

def test_create_project_ok(client, user_factory):
    owner = user_factory(email="owner1@example.com")
    payload = {
        "name": "Alpha",
        "description": "Premier projet",
        "status": "active",
        "owner_id": owner.id,
    }
    r = client.post("/projects", json=payload)
    assert r.status_code == HTTPStatus.CREATED, r.text
    body = r.json()
    assert body["name"] == "Alpha"
    assert body["description"] == "Premier projet"
    assert body["status"] == "active"
    assert body["owner_id"] == owner.id

def test_list_projects(client, user_factory):
    # crée 2 projets via l'API
    o = user_factory(email="owner2@example.com")
    client.post("/projects", json={"name": "P1", "owner_id": o.id})
    client.post("/projects", json={"name": "P2", "owner_id": o.id})

    r = client.get("/projects")
    assert r.status_code == HTTPStatus.OK
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    names = [p["name"] for p in data]
    assert "P1" in names and "P2" in names

def test_get_project_ok(client, user_factory):
    o = user_factory(email="owner3@example.com")
    r_create = client.post("/projects", json={"name": "Solo", "owner_id": o.id})
    pid = r_create.json()["id"]

    r = client.get(f"/projects/{pid}")
    assert r.status_code == HTTPStatus.OK
    assert r.json()["name"] == "Solo"

def test_get_project_not_found(client):
    r = client.get("/projects/999999")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "Project not found"

def test_update_project_ok(client, user_factory):
    o = user_factory(email="owner4@example.com")
    r_create = client.post("/projects", json={"name": "Old", "owner_id": o.id})
    pid = r_create.json()["id"]

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

def test_delete_project_ok(client, user_factory):
    o = user_factory(email="owner5@example.com")
    r_create = client.post("/projects", json={"name": "Del", "owner_id": o.id})
    pid = r_create.json()["id"]

    r = client.delete(f"/projects/{pid}")
    assert r.status_code == HTTPStatus.NO_CONTENT

    r2 = client.get(f"/projects/{pid}")
    assert r2.status_code == HTTPStatus.NOT_FOUND

def test_delete_project_not_found(client):
    r = client.delete("/projects/111111")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "Project not found"
