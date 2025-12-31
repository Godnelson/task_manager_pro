import pytest

@pytest.mark.anyio
async def test_task_filters_pagination(client):
    await client.post("/auth/register", json={"email": "t@t.com", "password": "password123"})
    r = await client.post("/auth/login", json={"email": "t@t.com", "password": "password123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/categories", json={"name": "Gym"}, headers=headers)
    cat_id = r.json()["id"]

    # Create tasks
    for i in range(1, 6):
        await client.post("/tasks", json={
            "title": f"Task {i}",
            "description": "desc",
            "category_id": cat_id,
            "status": "todo" if i < 4 else "done",
            "priority": "high" if i % 2 == 0 else "med"
        }, headers=headers)

    r = await client.get("/tasks?page=1&page_size=2", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["page_size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2

    r = await client.get("/tasks?status=done", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 2

    r = await client.get("/tasks?q=Task 1", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1
