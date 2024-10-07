from datetime import datetime, timedelta


def get_now():
    return datetime.utcnow()


def get_current_datetime_public_news_formatted() -> str:
    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M")
    return formatted_datetime


def get_date_days_ago(days: int = 3):
    days_ago = datetime.now() - timedelta(days=days)
    return days_ago


def refresh_time(site_dto_refresh_time: int = 0):
    try:
        minutes = int(site_dto_refresh_time)
        seconds = minutes * 60
        if not seconds:
            raise ValueError("Incorrect refresh time format")

        next_update = datetime.now() + timedelta(seconds=seconds)
        next_update_timestamp = int(next_update.timestamp())
        return next_update_timestamp
    except ValueError:
        raise ValueError("Incorrect refresh time format")


# Custom datetime parser
def parse_datetime(date_str: str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Invalid datetime format: {date_str}")
