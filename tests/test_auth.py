from http import HTTPStatus

from app.db.models import UserRole


def test_login_ok(client, user_factory):
    user_factory(email="test@example.com", password="secret")
    r = client.post("/auth/login", json={"email": "test@example.com", "password": "secret"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_ko(client):
    r = client.post("/auth/login", json={"email": "nobody@example.com", "password": "bad"})
    assert r.status_code == HTTPStatus.UNAUTHORIZED


def test_protected_access(client, user_factory):
    user_factory(email="role@example.com", role=UserRole.admin, password="pw")

    # login
    tok = client.post("/auth/login", json={"email": "role@example.com", "password": "pw"}).json()[
        "access_token"
    ]

    # appel d’une route protégée (adapte l’URL à ta route protégée)
    r = client.get("/projects", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200
