# import pytest
#
# from app.schema.base_schema import MessageResponseBase
# from app.schema.product_schema import ProductResponseSchema, ProductPublic
# from tests.test_api.test_v1.test_mock.mock_products import mock_products_data
# from tests.test_api.test_v1.test_endpoints.test_auth import mock_login  # noqa
#
#
# # @pytest.mark.dependency()
# # @pytest.mark.asyncio
# # async def test_news_timer_success():
# #     await container.news_timer_service().run_task()
# #     assert True
#
#
# # @pytest.mark.dependency(depends=['test_news_timer_success'])
# @pytest.mark.order(3)
# @pytest.mark.asyncio
# class TestProducts:
#     @pytest.mark.parametrize(
#         "method, endpoint, header, data, expected_status, expected_response, expected_response_type",
#         [
#             ("post", "/api/v1/products", "valid_auth_headers", "valid_creation_data", 201, None, ProductPublic),
#             ("post", "/api/v1/products", "valid_auth_headers", "invalid_creation_data", 422, None, MessageResponseBase),
#             ("post", "/api/v1/products", None, "valid_creation_data", 403, "Not authenticated", MessageResponseBase),
#             ("get", "/api/v1/products", None, None, 200, None, ProductResponseSchema),
#             ("get", "/api/v1/products?page=1&limit=3", None, None, 200, None, ProductResponseSchema),
#         ]
#     )
#     async def test(self, async_client, mock_login, method, endpoint, header, data, expected_status, expected_response, expected_response_type):
#         headers, data = mock_products_data(headers=header, data=data, mock_login=mock_login)
#
#         # async for client in async_client:
#         if method == "get":
#             response = await async_client.get(endpoint, headers=headers)
#             assert len(response.json()) > 1
#         elif method == "put":
#             response = await async_client.put(endpoint, headers=headers, json=data)
#         elif method == "delete":
#             response = await async_client.delete(endpoint, headers=headers)
#         elif method == "patch":
#             response = await async_client.patch(endpoint, headers=headers, json=data)
#         else:
#             response = await async_client.post(endpoint, headers=headers, json=data)
#
#         print(f"TestProducts response ====================== {response}")
#         assert response.status_code == expected_status
#         if expected_response_type:
#             assert expected_response_type(**response.json())
#         if expected_response:
#             assert str(expected_response) in str(response.json())
