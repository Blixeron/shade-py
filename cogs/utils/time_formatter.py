import dateutil.parser
import calendar

def iso_to_timestamp(date):
    iso = dateutil.parser.parse(date)
    timestamp = iso.timestamp()

    return timestamp

def utc_to_timestamp(date):
    timestamp = calendar.timegm(date.utctimetuple())

    return timestamp
