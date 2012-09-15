import re
from datetime import datetime

from cronjob import CronJob


class CronTab(object):
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
        zipped.sort(key=lambda x: x[1])

        for job, time, delta in zipped:
            print time.strftime("%b %d, %Y at %I:%M %p")
            print "({0} from now)".format(delta)
            print "    " + job.command
            print


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.__stderr__.write("{0}: Usage: {0} filename\n"
                .format(sys.argv[0]))
        sys.exit(-1)
    filename = sys.argv[1]
    
    file_ = open(filename)
    crontab = CronTab(file_)
    file_.close()
    crontab.print_next_times()
