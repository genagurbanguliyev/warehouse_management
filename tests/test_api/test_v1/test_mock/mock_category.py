from typing import Any


def mock_category_data(headers: str | None, data: str | None, mock_login: Any | None) -> tuple | None:
    token = None
    if mock_login is not None:
        token = mock_login
    mock_data = {
        "valid_auth_headers": {
            "Authorization": f"Bearer {token}"
        },
        "valid_data": {
            "name_tm": "Esasy Habarlar",
            "name_ru": "Главные новости",
            "parent_id": None,
        },
        "invalid_data": {
            "title": "Turkmenportal",
            "site_url": "https://www.turkmenportal.com",
            "invalid_key": 60
        },
        "valid_sort_data": {
            "categories": [
                {
                    "category_id": 1,
                    "sort": 2
                }
            ]
        },
        "null_variable": None,
    }

    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]
    return headers, data
