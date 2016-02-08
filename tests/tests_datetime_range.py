import unittest
from datetime import datetime, time, date, timedelta
from booking_engine.datetime_range import (
    by_timedelta_range, by_time_range, is_same_date, overlaps, contains,
    end_after_or_eq, merge_ranges
)


class TestDateTimeRange(unittest.TestCase):

    def setUp(self):
        pass

    def test_by_timedelta_range(self):
        timedelta_range = (
            timedelta(minutes=65),
            timedelta(hours=1, minutes=20)
        )
        dt = datetime(year=2016, day=28, month=2, hour=10, minute=10)

        expected_dt_range = (
            datetime(year=2016, day=28, month=2, hour=11, minute=15),
            datetime(year=2016, day=28, month=2, hour=11, minute=30)
        )

        self.assertEqual(by_timedelta_range(timedelta_range, dt),
                         expected_dt_range)

    def test_by_time_range(self):
        time_range = time(hour=9, minute=20), time(13, minute=30)
        d = date(year=2016, month=2, day=28)

        expected_dt_range = (
            datetime(year=2016, day=28, month=2, hour=9, minute=20),
            datetime(year=2016, day=28, month=2, hour=13, minute=30)
        )

        self.assertEqual(by_time_range(time_range, d), expected_dt_range)

    def test_by_time_range_that_span_tomorrow(self):
        time_range = time(hour=21, minute=30), time(4, minute=30)
        d = date(year=2016, month=2, day=28)

        expected_dt_range = (
            datetime(year=2016, day=28, month=2, hour=21, minute=30),
            datetime(year=2016, day=29, month=2, hour=4, minute=30)
        )

        self.assertEqual(by_time_range(time_range, d), expected_dt_range)

    def test_by_time_range_force_span_tomorrow(self):
        time_range = time(hour=9, minute=20), time(13, minute=30)
        d = date(year=2016, month=2, day=28)

        expected_dt_range = (
            datetime(year=2016, day=28, month=2, hour=9, minute=20),
            datetime(year=2016, day=29, month=2, hour=13, minute=30)
        )

        self.assertEqual(by_time_range(time_range, d, span_tomorrow=True),
                         expected_dt_range)

    def test_is_same_date_with_same_dates(self):
        dt_range = (
            datetime(year=2016, day=29, month=2,
                     hour=22, minute=40, second=11),
            datetime(year=2016, day=29, month=2,
                     hour=13, minute=22, second=13)
        )

        assert is_same_date(dt_range)

    def test_is_same_date_with_different_dates(self):
        dt_range = (
            datetime(year=2016, day=29, month=2,
                     hour=22, minute=40, second=11),
            datetime(year=2016, day=28, month=2,
                     hour=22, minute=40, second=11)
        )

        assert not is_same_date(dt_range)

    def test_overlaps_that_overlapped(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=10, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=10, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=22, second=12)
        )

        # also test that commutative property works :-/
        assert overlaps(dt_range_1, dt_range_2)
        assert overlaps(dt_range_2, dt_range_1)

    def test_overlaps_that_not_overlapped(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=10, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=12, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=22, second=12)
        )

        # also test that commutative property works :-/
        assert not overlaps(dt_range_1, dt_range_2)
        assert not overlaps(dt_range_2, dt_range_1)

    def test_overlaps_extremes_equals(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=10, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=22, second=12)
        )

        # also test that commutative property works :-/
        assert not overlaps(dt_range_1, dt_range_2)
        assert not overlaps(dt_range_2, dt_range_1)

    def test_overlaps_with_same_range(self):
        dt_range = (
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=10, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10)
        )

        assert overlaps(dt_range, dt_range)

    def test_contains_that_contains(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=0, second=0)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=22, second=12)
        )

        # if range is contained (and ranges are different) the opposite
        # is necessarily false
        assert contains(dt_range_1, dt_range_2)
        assert not contains(dt_range_2, dt_range_1)

    def test_contains_that_not_contains(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=0, second=0)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=15, minute=22, second=12)
        )

        assert not contains(dt_range_1, dt_range_2)

    def test_contains_with_same_range(self):
        dt_range = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=0, second=0)
        )

        assert contains(dt_range, dt_range)

    def test_ends_after_or_eq_that_ends_after(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=12, minute=0, second=0)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=22, second=12)
        )

        assert end_after_or_eq(dt_range_1, dt_range_2)

    def test_ends_after_or_eq_with_same_end(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=6, second=6)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=6, second=6)
        )

        assert end_after_or_eq(dt_range_1, dt_range_2)

    def test_ends_after_or_eq_thath_ends_before(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=6, second=6)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=6, second=6)
        )

        assert not end_after_or_eq(dt_range_1, dt_range_2)

    def test_merge_ranges(self):
        dt_range_1 = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=9, minute=6, second=6)
        )
        dt_range_2 = (
            datetime(year=2016, day=29, month=2,
                     hour=10, minute=20, second=10),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=6, second=6)
        )

        expected_dt_range = (
            datetime(year=2016, day=29, month=2,
                     hour=6, minute=0, second=0),
            datetime(year=2016, day=29, month=2,
                     hour=11, minute=6, second=6)
        )

        self.assertEqual(merge_ranges(dt_range_1, dt_range_2),
                         expected_dt_range)
