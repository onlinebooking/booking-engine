import unittest
from datetime import date, datetime
from booking_engine.time_util import (
    parse_date, format_date, date_with_year, start_of_day,
    tomorrow, yesterday, start_of_tomorrow, start_of_yesterday
)


class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_date(self):
        self.assertEqual(parse_date('2015-02-22'),
                         date(year=2015, month=2, day=22))

    def test_format_date(self):
        self.assertEqual(format_date(date(year=2015, month=2, day=22)),
                         '2015-02-22')

    def test_date_with_year(self):
        self.assertEqual(date_with_year(2015, date(year=4, month=2, day=22)),
                         date(year=2015, month=2, day=22))

    def test_date_with_year_29_feb_leap_year(self):
        self.assertEqual(date_with_year(2016, date(year=4, month=2, day=29)),
                         date(year=2016, month=2, day=29))

    def test_date_with_year_29_feb_not_leap_year(self):
        self.assertEqual(date_with_year(2015, date(year=4, month=2, day=29)),
                         None)

    def test_start_of_day_with_date(self):
        d = date(year=2016, month=2, day=29)
        expected_dt = datetime(year=2016, month=2, day=29,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_day(d), expected_dt)

    def test_start_of_day_with_datetime(self):
        dt = datetime(year=2016, month=2, day=29, hour=8, minute=58)
        expected_dt = datetime(year=2016, month=2, day=29,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_day(dt), expected_dt)

    def test_tomorrow_with_date(self):
        d = date(year=2016, month=2, day=29)
        expected_d = date(year=2016, month=3, day=1)
        self.assertEqual(tomorrow(d), expected_d)

    def test_tomorrow_with_datetime(self):
        dt = datetime(year=2016, month=2, day=29, hour=8, minute=58)
        expected_dt = datetime(year=2016, month=3, day=1,
                               hour=8, minute=58, second=0, microsecond=0)
        self.assertEqual(tomorrow(dt), expected_dt)

    def test_yesterday_with_date(self):
        d = date(year=2015, month=3, day=1)
        expected_d = date(year=2015, month=2, day=28)
        self.assertEqual(yesterday(d), expected_d)

    def test_start_of_tomorrow_with_date(self):
        d = date(year=2016, month=2, day=29)
        expected_dt = datetime(year=2016, month=3, day=1,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_tomorrow(d), expected_dt)

    def test_start_of_tomorrow_with_datetime(self):
        dt = datetime(year=2016, month=2, day=29, hour=22, minute=33, second=9)
        expected_dt = datetime(year=2016, month=3, day=1,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_tomorrow(dt), expected_dt)

    def test_start_of_yesterday_with_date(self):
        d = date(year=2016, month=1, day=1)
        expected_dt = datetime(year=2015, month=12, day=31,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_yesterday(d), expected_dt)

    def test_start_of_yesterday_with_datetime(self):
        dt = datetime(year=2016, month=2, day=29, hour=22, minute=33, second=9)
        expected_dt = datetime(year=2016, month=2, day=28,
                               hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(start_of_yesterday(dt), expected_dt)
