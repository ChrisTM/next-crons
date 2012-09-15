import re
from fieldparsers import Parse

nicknames = {
    '@yearly':   "0 0 1 1 *",
    '@annually': "0 0 1 1 *",
    '@monthly':  "0 0 1 * *",
    '@weekly':   "0 0 * * 0",
    '@daily':    "0 0 * * *",
    '@hourly':   "0 * * * *",
}

class CronJob(object):
    def __init__(self, line):
        # matches five fields separated by whitespace and then everything else
        # (the command)
        match = re.match(r'^(\S*)\s+(\S*)\s+(\S*)\s+(\S*)\s+(\S*)\s+(.*)$', line);

        self.minutes = Parse.minutes(match.group(1))
        self.hours = Parse.hours(match.group(2))
        self.days_of_month = Parse.days_of_month(match.group(3))
        self.months = Parse.months(match.group(4))
        self.days_of_week = Parse.days_of_week(match.group(5))

        self.command = match.group(6)


if __name__ == '__main__':
    c = CronJob('* * * * * awesome-command somefilename');
    print c.minutes, c.hours, c.days_of_month, c.months, c.days_of_week
