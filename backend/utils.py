import re
from datetime import datetime


def clean_number(value):
    if value is None:
        return 0.0

    # Remove everything except digits and dot
    value = re.sub(r"[^\d.]", "", str(value))

    try:
        return float(value)
    except:
        return 0.0


def clean_date(value):
    if not value:
        return None

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%d-%m-%Y",
        "%b %d",
        "%b %d, %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except:
            continue

    return None