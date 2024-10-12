from typing import Any


def mock_orders_data(headers: str | None, data: str | None, mock_login: Any | None) -> tuple | None:
    token = None
    if mock_login is not None:
        token = mock_login
    mock_data = {
        "valid_auth_headers": {
            "Authorization": f"Bearer {token}"
        },
        "null_variable": None,
        "valid_creation_data": {
            "delivery_address": "delivery Address of order",
            "products": []
        },
        "invalid_creation_data": {"quantity_in_stock": 10, "desc": "test product description"},
    }

    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]

    return headers, data
