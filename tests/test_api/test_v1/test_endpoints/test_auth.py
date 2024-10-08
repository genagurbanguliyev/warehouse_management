import pytest
from fastapi.testclient import TestClient

from httpx import AsyncClient

from tests.conftest import async_client, client # noqa
from app.core.config import configs
from app.schema.auth_schema import LoginSchema
from tests.test_api.test_v1.test_mock.mock_auth import mock_auth_data


@pytest.fixture(scope="function")
async def mock_login(async_client) -> str:
    data = LoginSchema(username=configs.DEFAULT_ADMIN, password=configs.DEFAULT_ADMIN_PASSWORD).model_dump()

    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     response = await ac.post("/auth/login", json=data, headers=headers)
    response = await async_client.post("/api/v1/auth/login", json=data)
    return response.json()


@pytest.fixture(scope="function")
async def mock_login_without_permissions(async_client) -> str:
    data = LoginSchema(username="client", password="client").model_dump()

    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     response = await ac.post("/auth/login", json=data, headers=headers)
    response = await async_client.post("/api/v1/auth/login", json=data)
    return response.json()


# @pytest.mark.order(2)
@pytest.mark.asyncio
class TestAuth:
    @pytest.mark.parametrize(
        "method, endpoint, headers, data, expected_status, expected_response, expected_response_type",
        [
            ("post", "/api/v1/auth/login", None, "login_valid_data", 201, None, str),
            ("post", "/api/v1/auth/login", None, "incorrect_password", 403, "Incorrect password", dict),
            ("post", "/api/v1/auth/login", None, "incorrect_username", 404, "Not found with given options", dict),
            ("post", "/api/v1/auth/registration", None, "registration_valid_body", 201, "test_admin", dict),
            ("get", "/api/v1/auth/me", "valid_auth_headers", "login_valid_data", 200, "admin", dict),
        ]
    )
    async def test(self, async_client, mock_login, method, endpoint, headers, data, expected_status, expected_response,
                   expected_response_type):
        headers, data = mock_auth_data(headers=headers, data=data, mock_login=mock_login)

        # async for client in async_client:
        if method == "get":
            response = await async_client.request(method, endpoint, headers=headers)
        elif method == "delete":
            response = await async_client.request(method, endpoint, headers=headers)
        elif method == "put":
            response = await async_client.request(method, endpoint, headers=headers, data=data)
        elif method == "patch":
            response = await async_client.request(method, endpoint, headers=headers, data=data)
        else:
            response = await async_client.request(method, endpoint, headers=headers, data=data)
#             response = await async_client.post(endpoint, headers=headers, json=data)

        print(f"Response TestAuth============= {response}")
        assert response.status_code == expected_status
        # assert isinstance(response.json(), expected_response_type)
        if expected_response:
            assert str(expected_response) in str(response.json())
