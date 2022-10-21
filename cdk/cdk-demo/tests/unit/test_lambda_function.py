from datetime import datetime, timedelta, timezone

from functions.lambda_function import convert_event_time


def test_convert_event_time():
    assert convert_event_time('2022-10-21T01:24:43Z') \
           == datetime(2022, 10, 21, 1, 24, 43, tzinfo=timezone(timedelta(hours=9), name='KST'))
