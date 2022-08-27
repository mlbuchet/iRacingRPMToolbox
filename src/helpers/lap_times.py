import datetime

def to_human_readable(lap_time):
    td = datetime.timedelta(seconds=lap_time)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{minutes}:{seconds:02}.{td.microseconds//1000:03}"
