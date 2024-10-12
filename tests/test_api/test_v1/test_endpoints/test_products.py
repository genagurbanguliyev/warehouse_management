import pytest

from app.schema.base_schema import MessageResponseBase
from app.schema.product_schema import ProductResponseSchema, ProductPublic
from tests.test_api.test_v1.mock.mock_products import mock_products_data
from tests.test_api.test_v1.test_endpoints.test_auth import mock_login  # noqa


@pytest.mark.order(4)
@pytest.mark.anyio
class TestProducts:
    @pytest.mark.parametrize(
        "method, endpoint, header, data_type, expected_status, expected_response, expected_response_type",
        [
            ("post", "/api/v1/products", "valid_auth_headers", "valid_creation_data", [201, 409], None, ProductPublic),
            ("post", "/api/v1/products", "valid_auth_headers", "invalid_creation_data", [422], None, MessageResponseBase),
            ("post", "/api/v1/products", None, "valid_creation_data", [403], "Not authenticated", MessageResponseBase),
            ("get", "/api/v1/products", None, None, [200], None, ProductResponseSchema)
        ]
    )
    async def test(self, async_client, mock_login, method, endpoint, header, data_type, expected_status, expected_response, expected_response_type):
        headers, data = mock_products_data(headers=header, data=data_type, mock_login=mock_login)

        if method == "get":
            response = await async_client.get(endpoint, headers=headers)
        elif method == "delete":
            response = await async_client.request(method, endpoint, headers=headers)
        else:
            response = await async_client.request(method, endpoint, headers=headers, json=data)

        assert response.status_code in expected_status
