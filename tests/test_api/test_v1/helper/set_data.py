from typing import Any


def true_data(data: Any, valid_data, invalid_data) -> dict:
    # Map string to the actual headers and data
    if data == "valid_data":
        data = valid_data
    elif data == "invalid_data":
        data = invalid_data

    return data
