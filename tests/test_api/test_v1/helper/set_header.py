def check_response_type(headers: str, test_get_captcha) -> dict:
    hash_value, captcha_value = test_get_captcha()
    print("Captcha values======================================================= ", hash_value, captcha_value)
    valid_captcha_headers = {
        "c-hash": hash_value,
        "captcha": captcha_value,
    }
    invalid_captcha_headers = {
        "c-hash": hash_value,
        "captcha": "captcha_value",
    }

    # Map string to the actual headers and data
    if headers == "valid_captcha_headers":
        headers = valid_captcha_headers
    elif headers == "invalid_captcha_headers":
        headers = invalid_captcha_headers

    return headers
