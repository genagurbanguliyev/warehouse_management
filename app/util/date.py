from datetime import datetime


def get_now():
    return datetime.utcnow()


def parse_datetime(date_str: str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Invalid datetime format: {date_str}")
