import pytest


@pytest.mark.asyncio
async def test_create_task_no_title_422(client, auth_header):
    r = await client.post("/tasks", json={"priority": 1},
                          headers=auth_header)
    assert r.status_code == 422
