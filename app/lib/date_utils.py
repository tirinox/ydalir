from datetime import datetime, timedelta, date

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
YEAR = 365 * DAY


def now_ts() -> float:
    # don't use utcnow() since timestamp() does this conversion
    return datetime.now().timestamp()


def now_ts_utc() -> float:
    return datetime.utcnow().timestamp()


def full_years_old_ts(birth_ts, today_ts=None) -> int:
    today_ts = today_ts or now_ts_utc()
    today = datetime.utcfromtimestamp(today_ts)
    birth_date = datetime.utcfromtimestamp(birth_ts)
    today_tuple = (today.month, today.day, today.hour, today.minute)
    birth_tuple = (birth_date.month, birth_date.day, birth_date.hour, birth_date.minute)
    yo = today.year - birth_date.year - int(today_tuple < birth_tuple)
    return max(0, yo)


def seconds_diff(t1: datetime, t2: datetime) -> float:
    return (t1 - t2).total_seconds()


def append_if_not_zero(acc, val, denom, translate, plural=True):
    if not val:
        return acc
    else:
        denom = (denom if val == 1 else f'{denom}s') if plural else denom
        denom = translate(denom)
        return "{} {} {}".format(acc, val, denom)


def seconds_human(seconds, translate=None, max_step=0) -> str:
    if seconds is None:
        return 'None'

    seconds = int(seconds)

    def tr(key):
        return translate.get(key, key) if translate else key

    if seconds == 0:
        return tr('just now')

    if seconds < 0:
        return '-' + seconds_human(-seconds, translate, max_step)

    if max_step:
        seconds = seconds // max_step * max_step

    minutes = (seconds // 60)
    hours = (minutes // 60)
    days = (hours // 24)
    months = (days // 30)
    years = days // 365

    s = append_if_not_zero('', years, 'year', tr)
    s = append_if_not_zero(s, months % 12, 'month', tr)
    s = append_if_not_zero(s, (days % 365) % 30, 'day', tr)
    if not months:
        s = append_if_not_zero(s, hours % 24, 'hour', tr)
    if not days:
        s = append_if_not_zero(s, minutes % 60, 'min', tr, plural=False)
    if not hours:
        s = append_if_not_zero(s, seconds % 60, 'sec', tr, plural=False)
    return s.strip()


LONG_AGO = datetime(1980, 1, 1)

NUMBER_CHARS = [chr(i + ord('0')) for i in range(10)] + ['.']
WHITE_SPACE_CHARS = [' ', ',', ';', ':', '\t', '/']


def parse_timespan_to_seconds(span: str, do_float=True):
    try:
        return float(span) if do_float else int(span)
    except ValueError:
        result = 0
        str_for_number = ''
        for symbol in span:
            symbol = symbol.lower()
            if symbol in ['d', 'h', 'm', 's']:
                if str_for_number:
                    try:
                        number = float(str_for_number) if do_float else int(str_for_number)
                    except ValueError:
                        return 'Error! Invalid number: {}'.format(str_for_number)
                    else:
                        multipliers = {
                            's': 1,
                            'm': MINUTE,
                            'h': HOUR,
                            'd': DAY
                        }
                        result += multipliers[symbol] * number
                    finally:
                        str_for_number = ''
                else:
                    return 'Error! Must be some digits before!'
            elif symbol in NUMBER_CHARS:
                str_for_number += symbol
            elif symbol in WHITE_SPACE_CHARS:
                pass
            else:
                return 'Error! Unexpected symbol: {}'.format(symbol)

        if str_for_number:
            return 'Error! Unfinished component in the end: {}'.format(str_for_number)

        return result


def format_time_ago(duration_sec, max_time=30 * DAY, translate=None):
    def tr(key):
        return translate.get(key, key) if translate else key

    if duration_sec is None or duration_sec == 0:
        return tr('never')
    elif abs(duration_sec) < 5:
        return tr('just now')
    elif abs(duration_sec) > max_time:
        return tr('long-long ago')
    else:
        return f'{seconds_human(duration_sec, translate=translate)} {tr("ago")}'


def format_time_ago_short(d, now=None):
    now = now if now is not None else now_ts()
    seconds = int(d - now)
    if seconds < 0:
        return "-" + format_time_ago_short(now, d)

    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    days = f'{days}d ' if days else ''
    minutes %= 60
    hours %= 24
    return f'{days}{hours:02}:{minutes:02}'


def today_str(prec='full'):
    now = datetime.now()
    if prec == 'day':
        fmt = "%d-%m-%Y"
    elif prec == 'hour':
        fmt = "%d-%m-%Y--%H"
    elif prec == 'minute':
        fmt = "%d-%m-%Y--%H-%M"
    else:
        fmt = "%d-%m-%Y--%H-%M-%S"
    return now.strftime(fmt)


def days_ago_noon(days_ago, now=None, hour=12, tz=None) -> datetime:
    now = now or datetime.now(tz=tz)
    day_back = now - timedelta(days=days_ago)
    day_back_noon = day_back.replace(hour=hour, minute=0, second=0, microsecond=0)
    return day_back_noon


def day_to_key(day: date, prefix=''):
    if day is None:
        day = datetime.now().date()
    return f'{prefix}:{day.year}.{day.month}.{day.day}'


def date_parse_rfc_z_no_ms(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")


def date_parse_rfc(s: str):
    s = s.rstrip('Z')
    s = s[:-3]
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")


def discard_time(dt: datetime):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
