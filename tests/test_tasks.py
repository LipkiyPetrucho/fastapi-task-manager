import pytest


@pytest.mark.asyncio
async def test_task_crud_flow(client, auth_header):
    # --- создание ---
    payload = {"title": "demo", "description": "test", "priority": 2}
    r = await client.post("/tasks", json=payload, headers=auth_header)
    assert r.status_code == 201
    task = r.json()
    task_id = task["id"]
    assert task["title"] == "demo"

    # --- обновление ---
    r = await client.put(
        f"/tasks/{task_id}", json={"status": "done"}, headers=auth_header
    )
    print(r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()["status"] == "done"

    # --- список ---
    r = await client.get("/tasks", headers=auth_header)
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id

    # --- поиск ---
    r = await client.get("/tasks/search", params={"q": "demo"}, headers=auth_header)
    assert r.status_code == 200
    assert r.json()[0]["id"] == task_id
