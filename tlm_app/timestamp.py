"""
Timestamp utils
"""

from datetime import datetime, timezone, timedelta

TIME_UNIT = 8e-9

# Satellite control system time started from January 1, 2014 00:00:00 (UTC + 8)
BEIJING_TIME = timezone(timedelta(hours=8))
SCS_EPOCH = datetime(2014, 1, 1, tzinfo=BEIJING_TIME).timestamp()


def timestamp_to_unixtime(tstamp: int) -> float:
    """
    Converts CU timestamps to Unix time
    """
    return TIME_UNIT * tstamp + SCS_EPOCH
