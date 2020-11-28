from datetime import date, timedelta


def get_working_bars(start: date, end: date) -> int:
    if start > end:
        return -1
    sw, ew = start.weekday(), end.weekday()
    s1 = start - timedelta(days=sw)
    e1 = end - timedelta(days=ew)
    s = (e1 - s1).days // 7 * 5
    t = ew - sw
    if sw == 6:
        t += 1
    if ew == 6:
        t -= 1
    return s + t