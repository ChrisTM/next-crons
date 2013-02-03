import re
from datetime import datetime

from cronjob import CronJob

class CronTab(object):
    """Represents a collection of cronjobs, AKA cron table or crontab."""
    def __init__(self, lines):
        self.jobs = []

        for line in lines:
            line = line.strip()
            try:
                self.jobs.append(CronJob(line))
            except ValueError:
                # CronJob raises a ValueError if the line doesn't look right.
                # This could be a comment, blank line, or environment setting.
                pass

    def print_next_times(self):
        now = datetime.now()
        jobs = self.jobs
        times = [job.next_time(now) for job in jobs]
        deltas = [time - now for time in times]

        zipped = zip(jobs, times, deltas)
        # sort by time
        zipped.sort(key=lambda x: x[1])

        for job, time, delta in zipped:
            print time.strftime("%b %d, %Y at %I:%M %p")
            print "({0} from now)".format(delta)
            print "    " + job.command
            print
