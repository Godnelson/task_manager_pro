import pytest

@pytest.mark.anyio
async def test_register_login_refresh_logout(client):
    r = await client.post("/auth/register", json={"email": "a@a.com", "password": "password123"})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "a@a.com"

    r = await client.post("/auth/login", json={"email": "a@a.com", "password": "password123"})
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    r = await client.get("/health")
    assert r.status_code == 200

    r = await client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r.status_code == 200
    new_tokens = r.json()
    assert new_tokens["access_token"] != tokens["access_token"]

    r = await client.post("/auth/logout", json={"refresh_token": new_tokens["refresh_token"]})
    assert r.status_code == 200
    assert r.json()["ok"] is True
