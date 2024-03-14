import pytest

from app.service_layer.users.utils import create_user


@pytest.fixture(autouse=True)
async def create_users(db_session):
    await create_user(db_session, "user1@example.com", "1234")
    await create_user(db_session, "user2@example.com", "1234")


async def login_user(async_client, email):
    request_data = {"username": email, "password": "1234"}
    response = await async_client.post("/auth/jwt/login", data=request_data)
    return response.json()["access_token"]


@pytest.mark.anyio
async def test_unauthorized_get(async_client):
    response = await async_client.get("/ecg/00000000-0000-0000-0000-000000000000/insights")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.anyio
async def test_unauthorized_post(async_client):
    response = await async_client.post("/ecg", json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.anyio
async def test_process_ecg(async_client):
    token = await login_user(async_client, "user1@example.com")
    ecg_data = {
        "id": "c7f1bb95-b665-4083-b983-8d24281c1ad6",
        "date": "2024-03-12T06:30:34.337937",
        "leads": [
            {
                "name": "I",
                "number_of_samples": 4,
                "signal": [9, -7, 3, 0, 5, -5, -1, 7, 0, 3, -3, -7, 7, 3, 9, -4, -8, -8, -9, 1]
            },
            {
                "name": "II",
                "signal": [-1, 3, -4, 0, 8, -6, 4, 3, 3, -6, -9, -6, 8, -2, -4, 2, 4, -3, -1, -1]
            }
        ]
    }
    response = await async_client.post("/ecg", json=ecg_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["id"] == "c7f1bb95-b665-4083-b983-8d24281c1ad6"


@pytest.mark.anyio
async def test_ecg_already_exists(async_client):
    await test_process_ecg(async_client)
    token = await login_user(async_client, "user1@example.com")
    ecg_data = {
        "id": "c7f1bb95-b665-4083-b983-8d24281c1ad6",
        "date": "2024-03-12T06:30:34.337937",
        "leads": [
            {
                "name": "II",
                "signal": [-1, 3, -4, 0, 8, -6, 4, 3, 3, -6, -9, -6, 8, -2, -4, 2, 4, -3, -1, -1]
            }
        ]
    }
    response = await async_client.post("/ecg", json=ecg_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "ECG_ALREADY_EXISTS"


@pytest.mark.anyio
async def test_ecg_not_found(async_client):
    token = await login_user(async_client, "user1@example.com")
    response = await async_client.get(
        "/ecg/c7f1bb95-b665-4083-b983-8d24281c1ad6/insights", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "ECG_NOT_FOUND"


@pytest.mark.anyio
async def test_get_ecg_insights(async_client):
    await test_process_ecg(async_client)
    token = await login_user(async_client, "user1@example.com")
    response = await async_client.get(
        "/ecg/c7f1bb95-b665-4083-b983-8d24281c1ad6/insights", headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == "c7f1bb95-b665-4083-b983-8d24281c1ad6"
    assert data["leads"][0]["insights"]["number_of_zero_crossing"] == 8
    assert data["leads"][1]["insights"]["number_of_zero_crossing"] == 10


@pytest.mark.anyio
async def test_forbidden_ecg_insights(async_client):
    await test_process_ecg(async_client)
    token = await login_user(async_client, "user2@example.com")
    response = await async_client.get(
        "/ecg/c7f1bb95-b665-4083-b983-8d24281c1ad6/insights", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"
