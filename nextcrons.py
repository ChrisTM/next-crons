#! /usr/bin/env python
"""
A client application that uses CronTab to tell you which cron jobs are
scheduled to be executed next
"""

from crontab import CronTab

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
