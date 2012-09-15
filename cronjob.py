import re
from datetime import datetime, timedelta

from fieldparsers import Parse

nicknames = {
    '@yearly':   "0 0 1 1 *",
    '@annually': "0 0 1 1 *",
    '@monthly':  "0 0 1 * *",
    '@weekly':   "0 0 * * 0",
    '@daily':    "0 0 * * *",
    '@hourly':   "0 * * * *",
}

def step_month(dt):
    # a month is not always the same duration, so we cannot just add a
    # timedelta
    month = (dt.month % 12) + 1
    dt = dt.replace(month=month, day=0, hour=0, minute=0)

    # if the months wrapped around to jan, the year also needs to increment
    if month == 1:
        next_year = dt.year + 1
        dt = dt.replace(year=next_year)

    return dt

def step_day(dt):
    dt += timedelta(days=1)
    dt = dt.replace(hour=0, minute=0)
    return dt

def step_hour(dt):
    dt += timedelta(hours=1)
    dt = dt.replace(minutes=0)
    return dt

def step_minute(dt):
    dt += timedelta(minutes=1)
    return dt

class CronJob(object):
    def __init__(self, line):
        # matches five fields separated by whitespace and then everything else
        # (the command)
        field = r'([\w\d,*/-]+)' # one or more alpha, digit, *, /, -
        whitespace = r'\s+' # one or more whitespace (separates fields)
        command = r'(.*)' # everything else goes to the command
        regex = '^' + (field + whitespace) * 5 + command + '$'
        match = re.match(regex, line);
        if match is None:
            raise ValueError('The line {0} does not look line a cronjob.'.format(line));

        self.minutes = Parse.minutes(match.group(1))
        self.hours = Parse.hours(match.group(2))
        self.days_of_month = Parse.days_of_month(match.group(3))
        self.months = Parse.months(match.group(4))
        self.days_of_week = Parse.days_of_week(match.group(5))

        self.command = match.group(6)

    """
    Return True if the month, day/weekday, and hour fields in `dt` matches
    this cronjob.
    """
    def matches(self, dt):
        return (
            dt.minute in self.minutes and
            dt.hour in self.hours and
            dt.day in self.days_of_month and
            dt.month in self.months and
            # isoweekday uses 1-7 (mon-sun), but cron uses 0-6 (sun-sat)
            dt.isoweekday() % 6 in self.days_of_week
        )


    """
    Return the datetime object for when this cronjob will next fire

    Approach: we'll use a greedy brute-force approach. We start with a time
    value set to `now`, then repeatedly increment the time with the largest
    steps we can (month, day, hour, then minute) until we get a
    match with the job. This approach is simple and not too slow, taking at
    most ~12+31+24+60 = 127 steps and checks.
    """
    def next_time(self, now=None):
        time = now or datetime.now()
        # now shouldn't actually count as a /next/ time, so we bump it forward
        # to prevent now from being returned
        time = step_minute(time)
        while True:
            if time.month not in self.months:
                time = step_month(time)
                continue
            if time.day not in self.days_of_month:
                time = step_day(time)
                continue
            if time.isoweekday() % 6 not in self.days_of_week:
                time = step_day(time)
                continue
            if time.hour not in self.hours:
                time = step_hour(time)
                continue
            if time.minute not in self.minutes:
                time = step_minute(time)
                continue
            break
        return time

    """
    Return a generator of datetimes corresponding to the next times this job
    will fire
    """
    def next_times(self, now=None):
        while True:
            now = self.next_time(now)
            yield now
