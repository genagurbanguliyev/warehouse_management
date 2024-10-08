from typing import Any


def mock_sites_data(headers: str | None, data: str | None, mock_login: Any | None) -> tuple | None:
    token = None
    if mock_login is not None:
        token = mock_login
    mock_data = {
        "valid_auth_headers": {
            "Authorization": f"Bearer {token}"
        },
        "valid_data": {
            "title": "Turkmenportal",
            "site_url": "https://www.turkmenportal.com",
            "icon": "https://turkmenportal.com/themes/turkmenportal/img/logo_tp.png?v=1",
            "rss_tm": "https://turkmenportal.com/rss/tm",
            "rss_ru": "https://turkmenportal.com/rss",
            "refresh_time": 60
        },
        "invalid_data": {
            "title": "Turkmenportal",
            "site_url": "https://www.turkmenportal.com",
            "invalid_key": 60
        },
        "null_variable": None,
    }

    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]
    return headers, data
