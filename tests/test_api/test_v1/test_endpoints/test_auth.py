import pytest
from httpx import AsyncClient

from tests.test_api.test_v1.mock.mock_auth import mock_auth_data
from tests.conftest import async_client # noqa


@pytest.fixture
async def mock_login(async_client: AsyncClient):
    response = await async_client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    return response.json()


@pytest.mark.order(3)
@pytest.mark.anyio
class TestAuth:
    @pytest.mark.parametrize(
        "method, endpoint, headers, data_type, expected_status, expected_response, expected_response_type",
        [
            ("post", "/api/v1/auth/login", None, "login_valid_data", [201], None, str),
            ("post", "/api/v1/auth/login", None, "incorrect_password", [403], "Incorrect password", dict),
            ("post", "/api/v1/auth/login", None, "incorrect_username", [404], "Not found with given options", dict),
            ("post", "/api/v1/auth/registration", None, "registration_valid_body", [201, 409], "test_admin", dict),
            ("get", "/api/v1/auth/me", "valid_auth_headers", None, [200], "admin", dict),
        ]
    )
    async def test(self, async_client: AsyncClient, mock_login, method, endpoint, headers, data_type, expected_status, expected_response,
                   expected_response_type):
        headers, data = mock_auth_data(headers=headers, data=data_type, mock_login=mock_login)

        if method == "get":
            response = await async_client.request(method, endpoint, headers=headers)
        elif method == "delete":
            response = await async_client.request(method, endpoint, headers=headers)
        else:
            response = await async_client.request(method, endpoint, headers=headers, json=data)
#             response = await async_client.post(endpoint, headers=headers, json=data)

        print(f"Response TestAuth============= {response.json()}")
        assert response.status_code in expected_status
        # assert isinstance(response.json(), expected_response_type)
        # if expected_response:
        #     assert str(expected_response) in str(response.json())
