import calendar
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

KST = timezone(timedelta(hours=9), name='KST')


def convert_event_time(event_time: str) -> datetime:
    strptime = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
    return strptime.astimezone(tz=KST)


def handler(event, context=None):
    logging.Formatter.converter = lambda *args: datetime.now(tz=KST).timetuple()

    if 'time' in event:
        dt = convert_event_time(event['time'])
        logger.info(
            "Thanks for calling me on %s at %s.",
            calendar.day_name[dt.weekday()], dt.time().isoformat())

    logger.info("Full event: %s", event)
    logger.info("context: %s", context)

