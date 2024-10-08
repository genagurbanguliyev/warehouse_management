from typing import Any

from app.core.config import configs


def mock_auth_data(headers: str | None, data: str | None, mock_login: Any | None) -> tuple | None:
    token, hash_value, captcha_value = None, None, None
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
            "password": "incorrect"
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
            "name": "test_admin",
            "username": "test_admin4",
            "password": "test_password4",
            "role": "user"
        },
        "null_variable": None
    }
    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]

    return headers, data
