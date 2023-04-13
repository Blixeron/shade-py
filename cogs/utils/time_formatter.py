import dateutil.parser

import time
import calendar

def iso_to_timestamp(date):
    iso = dateutil.parser.parse(date)
    timestamp = time.mktime(iso.timetuple())

    return timestamp

def utc_to_timestamp(date):
    timestamp = calendar.timegm(date.utctimetuple())

    return timestamp
