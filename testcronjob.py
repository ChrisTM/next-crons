import unittest
from datetime import datetime

from cronjob import CronJob


class TestCronJob(unittest.TestCase):
    def setUp(self):
        pass

    def test_complex_command(self):
        job = CronJob('* * * * * grep -ri foobar / > out.txt')
        self.assertEquals(job.command, 'grep -ri foobar / > out.txt')

    def test_hourly(self):
        job = CronJob('0 * * * * command')
        self.assertEquals(job.minutes, [0])
        self.assertEquals(job.hours, range(0, 24))
        self.assertEquals(job.days_of_month, range(1, 32))
        self.assertEquals(job.months, range(1, 13))
        self.assertEquals(job.days_of_week, range(0, 7))

    def test_every_ten_minutes(self):
        job = CronJob('*/10 * * * * command')
        self.assertEquals(job.minutes, range(0, 60, 10))
        self.assertEquals(job.hours, range(0, 24))
        self.assertEquals(job.days_of_month, range(1, 32))
        self.assertEquals(job.months, range(1, 13))
        self.assertEquals(job.days_of_week, range(0, 7))

    def test_next_time(self):
        job = CronJob('*/10 * * * * command')

        now =      datetime(2012, 10, 19, 8,  5); # 8:05am
        exp_next = datetime(2012, 10, 19, 8, 10); # 8:10am
        obs_next = job.next_time(now)

        self.assertEquals(exp_next, obs_next)
