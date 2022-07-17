from datetime import datetime
from typing import Optional


def datetime_to_str(date_with_timezone: Optional[datetime]):
    if not date_with_timezone:
        return ""

    try:
        return f"{date_with_timezone:%Y-%m-%d}"
    except Exception:
        return date_with_timezone.__str__()
