import pytest

from app.service_layer.users.utils import create_user


@pytest.fixture(autouse=True)
async def create_users(db_session):
    await create_user(db_session, "admin@example.com", "1234", True)
    await create_user(db_session, "user1@example.com", "1234")


async def login_user(async_client, email):
    request_data = {"username": email, "password": "1234"}
    response = await async_client.post("/auth/jwt/login", data=request_data)
    return response.json()["access_token"]


@pytest.mark.anyio
async def test_unauthorized_register(async_client):
    response = await async_client.post("/auth/register", data={"username": "user2@example.com", "password": "1234"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.anyio
async def test_forbidden_register(async_client):
    token = await login_user(async_client, "user1@example.com")
    response = await async_client.post(
        "/auth/register", 
        data={"username": "user2@example.com", "password": "1234"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.anyio
async def test_register_ok(async_client):
    token = await login_user(async_client, "admin@example.com")
    response = await async_client.post(
        "/auth/register", 
        json={"email": "user2@example.com", "password": "1234"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "user2@example.com"


@pytest.mark.anyio
async def test_admin_forbidden_post(async_client):
    token = await login_user(async_client, "admin@example.com")
    ecg_data = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "date": "2024-03-14T15:06:03.081Z",
        "leads": [
            {
                "name": "I",
                "number_of_samples": 0,
                "signal": [0]
            }
        ]
    }
    response = await async_client.post("/ecg", json=ecg_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.anyio
async def test_admin_forbidden_get(async_client):
    token = await login_user(async_client, "admin@example.com")
    response = await async_client.get(
        "/ecg/00000000-0000-0000-0000-000000000000/insights", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

