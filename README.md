What does nextcrons do?
=======================
nextcrons will read a crontab file and tell you which cron jobs are scheduled
to be executed next.

How do I use nextcrons?
=======================
An example:

    $ python nextcrons.py crontabfile
    Sep 15, 2012 at 03:52 PM
    (0:01:00 from now)
        sh ~/jobs/job2.sh

    Sep 15, 2012 at 03:55 PM
    (0:04:00 from now)
        sh ~/jobs/job1.sh

    Sep 16, 2012 at 12:30 AM
    (8:39:00 from now)
        sh ~/jobs/job3.sh

What cron standard does this follow?
====================================
ISC Cron V4.1. See [the manpage](http://unixhelp.ed.ac.uk/CGI/man-cgi?crontab+5) for details.

Some things however, are unsupported:

  * nicknames like @weekly

Some non standard things are incidentally supported:
  
  * named ranges like `mon-wed` or `apr-aug`.


Can I use it programmatically?
==============================
Yes, but it's not too exciting because currently, the API only exists to do a
rather small task: find the next time a cron job will run.

Check out the docstrings for CronJob and CronTab for more info.
