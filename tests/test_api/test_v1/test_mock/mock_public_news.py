from typing import Any


def mock_public_news_data(headers: str | None, data: str | None, mock_login: Any | None, news: list | None = None) -> tuple | None:
    token = None
    if mock_login is not None:
        token = mock_login
    mock_data = {
        "valid_auth_headers": {
            "Authorization": f"Bearer {token}"
        },
        "invalid_data": {
            "title": "Turkmenportal",
            "site_url": "https://www.turkmenportal.com",
            "invalid_key": 60
        },
        "null_variable": None,
    }
    if news is not None:
        mock_data["valid_data"] = {
            "title": news[0]["title"],
            "desc": news[0]["desc"],
            "image": news[0]["image"],
            "pub_date": news[0]["pub_date"],
            "lang": news[0]["lang"],
            "categories": [
                {
                    "category_id": 1,
                    "sort": 1
                }
            ],
            "news_ids": [
                news[0]["id"], news[1]["id"], news[2]["id"]
            ]
        }

    if headers is not None:
        headers = mock_data[headers]
    if data is not None:
        data = mock_data[data]
    return headers, data
