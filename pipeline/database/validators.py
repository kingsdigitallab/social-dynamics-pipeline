from datetime import date, datetime
from typing import Optional, Union


def validate_date(value: Union[str, date, None]) -> Optional[date]:
    """Validate date fields"""
    if value is None or isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            # ISO 8601 format (YYYY-MM-DD)
            return date.fromisoformat(value)
        except ValueError:
            pass  # try next format

        try:
            # UK-style format (DD/MM/YYYY)
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as e:
            raise ValueError(
                "Date {} must be in YYYY-MM-DD or DD/MM/YYYY format.".format(value)
            ) from e
    raise TypeError("Date {} must be a string or date.".format(value))
