from typing import Any

from warehouse_management.core.config import configs


def mock_auth_data(headers: str | None, data: str | None, mock_login: Any | None) -> tuple | None:
    token = None
    if mock_login is not None:
        token = mock_login
    mock_data = {
        "valid_auth_headers": {
            "Authorization": f"Bearer {token}"
        },
        "login_valid_data": {
            "username": configs.DEFAULT_ADMIN,
            "password": configs.DEFAULT_ADMIN_PASSWORD
        },
        "incorrect_username": {
            "username": "incorrect_username",
            "password": configs.DEFAULT_ADMIN_PASSWORD
        },
        "incorrect_password": {
            "username": configs.DEFAULT_ADMIN,
            "password": "incorrect_password"
        },
        "invalid_values": {
            "uname": "invalid_keys",
            "pwd": "invalid"
        },
        "registration_valid_body": {
            "name": "test_client",
            "username": "test_client",
            "password": "test_client_password",
            "role": "client"
        },
        "null_variable": None
    }
    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]

    return headers, data
