from datetime import datetime, timezone 
from dateutil import parser


def to_iso_timestamp(timestamp: str) -> datetime:
    """
    Parses a timestamp string into a valid ISO-8601 timestamp.

    :param timestamp: The timestamp to parse.
    :return: The parsed timestamp.
    """

    dt = parser.parse(timestamp)
    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)