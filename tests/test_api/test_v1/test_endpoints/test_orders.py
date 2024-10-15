import pytest
from httpx import AsyncClient

from warehouse_management.schema.base_schema import MessageResponseBase
from warehouse_management.schema.order_schema import OrderResponseSchema
from tests.test_api.test_v1.mock.mock_orders import mock_orders_data
from tests.test_api.test_v1.test_endpoints.test_auth import mock_login  # noqa


@pytest.mark.order(5)
@pytest.mark.anyio
class TestOrder:
    @pytest.mark.parametrize(
        "method, endpoint, header, data_type, expected_status, expected_response, expected_response_type",
        [
            ("post", "/api/v1/orders", "valid_auth_headers", "valid_creation_data", [201, 400], None, MessageResponseBase),
            ("post", "/api/v1/orders", "valid_auth_headers", "invalid_creation_data", [422], None, MessageResponseBase),
            ("post", "/api/v1/orders", None, "valid_creation_data", [403], "Not authenticated", MessageResponseBase),
            ("get", "/api/v1/orders", "valid_auth_headers", None, [200], None, OrderResponseSchema),
        ]
    )
    async def test(self, async_client, mock_login, method, endpoint, header, data_type, expected_status, expected_response, expected_response_type):
        headers, data = mock_orders_data(headers=header, data=data_type, mock_login=mock_login)

        if method == "post" and endpoint == "/api/v1/orders" and data_type == "valid_creation_data":
            product_id = await self.get_products(async_client)
            if product_id is None:
                raise ValueError("There is no product in products table")
            else:
                data["products"].append({
                    "product_id": product_id,
                    "quantity": 10
                })

        if method == "get":
            response = await async_client.get(endpoint, headers=headers)
        elif method == "delete":
            response = await async_client.request(method, endpoint, headers=headers)
        else:
            response = await async_client.request(method, endpoint, headers=headers, json=data)

            if expected_response_type:
                assert expected_response_type(**response.json())

        assert response.status_code in expected_status
        # if expected_response:
        #     assert str(expected_response) in str(response.json())

    @staticmethod
    async def get_products(async_client: AsyncClient):
        response = await async_client.get("/api/v1/products")
        print(f"ppppppppppppppppppppppppppppppppppppppppppppppppppppppppp {response.json()}")
        pr = response.json().get("data", [])
        return pr[0]["id"] if len(pr) else None
