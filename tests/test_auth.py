import pytest

USER = {"name": "Ann", "email": "ann@test.com", "password": "secret123"}


@pytest.mark.asyncio
async def test_register_login_flow(client):
    # регистрация
    r = await client.post("/register", json=USER)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == USER["email"]

    # логин
    r = await client.post("/login", json=USER)
    assert r.status_code == 200
    tokens = r.json()
    assert {"access", "refresh"} <= tokens.keys()

    # refresh
    r = await client.post(f"/refresh?token={tokens['refresh']}")
    assert r.status_code == 200
    assert "access" in r.json()
    # # assert new_tokens["access"] != tokens["access"]
