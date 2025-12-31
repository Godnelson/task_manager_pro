import pytest

@pytest.mark.anyio
async def test_category_crud(client):
    await client.post("/auth/register", json={"email": "u@u.com", "password": "password123"})
    r = await client.post("/auth/login", json={"email": "u@u.com", "password": "password123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/categories", json={"name": "Work"}, headers=headers)
    assert r.status_code == 200
    cat = r.json()
    assert cat["name"] == "Work"

    r = await client.get("/categories", headers=headers)
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 1

    r = await client.patch(f"/categories/{cat['id']}", json={"name": "Deep Work"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Deep Work"

    r = await client.delete(f"/categories/{cat['id']}", headers=headers)
    assert r.status_code == 200
