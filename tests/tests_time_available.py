import unittest
from datetime import date, time, datetime
from booking_engine.util.time import tomorrow
from booking_engine.time_available import (
    defaulitize_availability, is_date_a_fixed_closing_date,
    is_date_a_special_closing_date, is_date_a_week_working_date,
    is_date_a_special_working_date, is_date_available,
    working_hours_of_date, working_hours_to_datetime_ranges,
    are_working_hours_contiguous, working_datetime_ranges_of_date,
)


class TestTimeAvailable(unittest.TestCase):

    def setUp(self):
        pass

    def test_defaulitize_availability_with_empty_dict(self):
        self.assertEqual(defaulitize_availability({}), {
            'fixed_closing_days': [],
            'special_closing_days': [],
            'week_working_hours': {},
            'special_working_hours': {},
        })

    def test_defaulitize_availability_filled_fixed_closing_days(self):
        self.assertEqual(defaulitize_availability({
            'fixed_closing_days': [
                date(year=4, month=2, day=2),
                date(year=4, month=12, day=25),
            ],
        }), {
            'fixed_closing_days': [
                date(year=4, month=2, day=2),
                date(year=4, month=12, day=25),
            ],
            'special_closing_days': [],
            'week_working_hours': {},
            'special_working_hours': {},
        })

    def test_defaulitize_availability_filled_special_closing_days(self):
        self.assertEqual(defaulitize_availability({
            'special_closing_days': [
                date(year=2016, month=2, day=2),
                date(year=2016, month=12, day=24),
            ],
        }), {
            'fixed_closing_days': [],
            'special_closing_days': [
                date(year=2016, month=2, day=2),
                date(year=2016, month=12, day=24),
            ],
            'week_working_hours': {},
            'special_working_hours': {},
        })

    def test_defaulitize_availability_filled_week_working_hours(self):
        self.assertEqual(defaulitize_availability({
            'week_working_hours': {
                1: [(time(hour=9), time(hour=10))],
                2: [(time(hour=9), time(hour=10))],
            }
        }), {
            'fixed_closing_days': [],
            'special_closing_days': [],
            'week_working_hours': {
                1: [(time(hour=9), time(hour=10))],
                2: [(time(hour=9), time(hour=10))],
            },
            'special_working_hours': {},
        })

    def test_defaulitize_availability_filled_special_working_hours(self):
        self.assertEqual(defaulitize_availability({
            'special_working_hours': {
                date(year=2016, month=2, day=4): [
                    (time(hour=6), time(hour=7)),
                    (time(hour=9), time(hour=12)),
                ]
            },
        }), {
            'fixed_closing_days': [],
            'special_closing_days': [],
            'week_working_hours': {},
            'special_working_hours': {
                date(year=2016, month=2, day=4): [
                    (time(hour=6), time(hour=7)),
                    (time(hour=9), time(hour=12)),
                ]
            },
        })

    def test_defaulitize_availability_filled_all(self):
        availability = {
            'fixed_closing_days': [date(year=4, month=2, day=2)],
            'special_closing_days': [date(year=2016, month=2, day=2)],
            'week_working_hours': {
                1: [(time(hour=9), time(hour=10))]
            },
            'special_working_hours': {
                date(year=1993, month=9, day=26): [
                    (time(hour=6), time(hour=7)),
                ],
            },
        }
        self.assertEqual(defaulitize_availability(availability), availability)

    def test_is_date_a_fixed_closing_date_with_a_compatible_date(self):
        assert is_date_a_fixed_closing_date(
            date(year=1999, month=12, day=29),
            [
                date(year=1999, month=12, day=28),
                date(year=1975, month=2, day=3),
                date(year=2004, month=2, day=29),
                date(year=4, month=12, day=29),
            ]
        )

    def test_is_date_a_fixed_closing_date_with_an_incompatible_date(self):
        assert not is_date_a_fixed_closing_date(
            date(year=2016, month=2, day=29),
            [
                date(year=1999, month=12, day=28),
                date(year=1975, month=2, day=3),
                date(year=2003, month=2, day=28),
                date(year=4, month=12, day=29),
            ]
        )

    def test_is_date_a_special_closing_date_with_a_compatible_date(self):
        assert is_date_a_special_closing_date(
            date(year=2016, month=12, day=29),
            [
                date(year=1999, month=12, day=28),
                date(year=1975, month=12, day=3),
                date(year=2004, month=2, day=29),
                date(year=4, month=12, day=29),
                date(year=2016, month=12, day=29),
            ]
        )

    def test_is_date_a_special_closing_date_with_an_incompatible_date(self):
        assert not is_date_a_special_closing_date(
            date(year=2016, month=12, day=29),
            [
                date(year=1999, month=12, day=28),
                date(year=1975, month=12, day=3),
                date(year=2004, month=2, day=29),
                date(year=4, month=12, day=29),
                date(year=2008, month=12, day=29),
            ]
        )

    def test_is_date_a_week_working_date_with_a_compatible_date(self):
        assert is_date_a_week_working_date(
            date(year=1993, month=9, day=26),
            {
                6: [(time(hour=9), time(hour=12))],
            }
        )

    def test_is_date_a_week_working_date_with_an_incompatible_date(self):
        assert not is_date_a_week_working_date(
            date(year=1990, month=10, day=3),
            {
                0: [(time(hour=9), time(hour=12))],
                1: [(time(hour=23), time(hour=2))],
                3: [(time(hour=8), time(hour=9))],
                6: [(time(hour=3), time(hour=5))],
            }
        )

    def test_is_date_a_special_working_date_with_a_compatible_date(self):
        assert is_date_a_special_working_date(
            date(year=1993, month=9, day=26),
            {
                date(year=1993, month=9, day=26): [
                    (time(hour=9), time(hour=12)),
                ],
            }
        )

    def test_is_date_a_special_working_date_with_an_incompatible_date(self):
        assert not is_date_a_special_working_date(
            date(year=1995, month=6, day=25),
            {
                date(year=1993, month=6, day=25): [
                    (time(hour=9), time(hour=12)),
                ],
                date(year=1995, month=6, day=24): [
                    (time(hour=1), time(hour=3)),
                ],
            }
        )

    def test_is_date_available_on_empty_availability(self):
        assert not is_date_available(date(year=2016, month=2, day=9), {})

    def test_is_date_available_special_closing_date(self):
        d = date(year=1993, month=9, day=26)
        wwh_ok = {
            d.weekday(): [(time(hour=9), time(hour=12))],
        }
        swh_ok = {
            d: [(time(hour=9), time(hour=12))],
        }

        # special_closing_days "wins" over
        # special_working_hours and week_working_hours
        assert not is_date_available(d, {
            'special_closing_days': [d],
            'special_working_hours': swh_ok,
            'week_working_hours': wwh_ok,
        })

    def test_is_date_available_special_working_date(self):
        d = date(year=1993, month=9, day=26)
        wwh_bad = {
            1: [(time(hour=9), time(hour=12))],
        }
        swh_ok = {
            d: [(time(hour=9), time(hour=12))],
        }
        # special_working_hours "wins" over
        # fixed_closing_days and week_working_hours
        assert is_date_available(d, {
            'special_working_hours': swh_ok,
            'fixed_closing_days': [d],
            'week_working_hours': wwh_bad,
        })

    def test_is_date_available_fixed_closing_date(self):
        d = date(year=1993, month=9, day=26)
        wwh_ok = {
            d.weekday(): [(time(hour=9), time(hour=12))],
        }
        # special_working_hours "wins" over
        # fixed_closing_days and week_working_hours
        assert not is_date_available(d, {
            'fixed_closing_days': [d],
            'week_working_hours': wwh_ok,
        })

    def test_is_date_available_week_working_date(self):
        good_date = date(year=1993, month=9, day=26)
        bad_date = date(year=1993, month=9, day=25)
        whs_sunday = {
            6: [(time(hour=9), time(hour=12))],
        }
        availability = {
            'week_working_hours': whs_sunday
        }

        # when other constrains are falsy is_date_available
        # has the same result as is_date_a_week_working_date
        self.assertEqual(is_date_available(good_date, availability),
                         is_date_a_week_working_date(good_date, whs_sunday))
        self.assertEqual(is_date_available(bad_date, availability),
                         is_date_a_week_working_date(bad_date, whs_sunday))

    def test_working_hours_of_date_special_hours(self):
        d = date(year=1993, month=9, day=26)
        wh_for_swh = [(time(hour=9), time(hour=12))]
        swh_ok = {
            d: wh_for_swh
        }
        wh_for_wwh = [(time(hour=18), time(hour=22))]
        wwh_ok = {
            d.weekday():  wh_for_wwh
        }
        # special_working_hours has more priority then week_working_hours
        self.assertEqual(working_hours_of_date(d, swh_ok, wwh_ok), wh_for_swh)

    def test_working_hours_of_date_weekly_hours(self):
        d = date(year=1993, month=9, day=26)
        wh_for_swh = [(time(hour=9), time(hour=12))]
        swh_bad = {
            date(year=2009, month=9, day=26): wh_for_swh
        }
        wh_for_wwh = [(time(hour=18), time(hour=22))]
        wwh_ok = {
            d.weekday():  wh_for_wwh
        }
        self.assertEqual(working_hours_of_date(d, swh_bad, wwh_ok), wh_for_wwh)

    def test_working_hours_of_date_empty(self):
        d = date(year=1993, month=9, day=26)
        wh_for_swh = [(time(hour=9), time(hour=12))]
        swh_bad = {
            date(year=2009, month=9, day=26): wh_for_swh
        }
        wh_for_wwh = [(time(hour=18), time(hour=22))]
        wwh_bad = {
            1:  wh_for_wwh
        }
        self.assertEqual(working_hours_of_date(d, swh_bad, wwh_bad), [])

    def test_working_hours_to_datetime_ranges(self):
        d = date(year=1993, month=9, day=26)
        wh = [
            (time(hour=9), time(hour=12)),
            (time(hour=18), time(hour=18)),
            (time(hour=21), time(hour=9)),
        ]
        self.assertEqual(working_hours_to_datetime_ranges(d, wh), [
            (
                datetime(year=1993, month=9, day=26, hour=9),
                datetime(year=1993, month=9, day=26, hour=12)
            ),
            (
                datetime(year=1993, month=9, day=26, hour=21),
                datetime(year=1993, month=9, day=27, hour=9)
            ),
        ])

    def test_working_hours_to_datetime_ranges_span_tomorrow(self):
        d = date(year=1993, month=9, day=26)
        wh = [
            (time(hour=9), time(hour=12)),
            (time(hour=18), time(hour=18)),
            (time(hour=21), time(hour=9)),
        ]
        r = working_hours_to_datetime_ranges(d, wh, span_tomorrow=True)
        self.assertEqual(r, [
            (
                datetime(year=1993, month=9, day=26, hour=9),
                datetime(year=1993, month=9, day=27, hour=12)
            ),
            (
                datetime(year=1993, month=9, day=26, hour=18),
                datetime(year=1993, month=9, day=27, hour=18)
            ),
            (
                datetime(year=1993, month=9, day=26, hour=21),
                datetime(year=1993, month=9, day=27, hour=9)
            ),
        ])

    def test_are_working_hours_contiguous_with_contiguous_working_hours(self):
        assert are_working_hours_contiguous([
            (time(hour=9), time(hour=12)),
            (time(hour=21), time(hour=0)),
        ], [
            (time(hour=0), time(hour=10)),
            (time(hour=21), time(hour=22)),
        ])

    def test_are_working_hours_contiguous_with_separeted_working_hours(self):
        assert not are_working_hours_contiguous([
            (time(hour=9), time(hour=12)),
            (time(hour=21), time(hour=23)),
        ], [
            (time(hour=0), time(hour=10)),
            (time(hour=21), time(hour=22)),
        ])
        assert not are_working_hours_contiguous([
            (time(hour=9), time(hour=12)),
            (time(hour=21), time(hour=0)),
        ], [
            (time(hour=1), time(hour=10)),
            (time(hour=21), time(hour=22)),
        ])
        assert not are_working_hours_contiguous([
            (time(hour=9), time(hour=12)),
            (time(hour=21), time(hour=0)),
        ], [])
        assert not are_working_hours_contiguous([], [
            (time(hour=0), time(hour=10)),
            (time(hour=21), time(hour=22)),
        ])
        assert not are_working_hours_contiguous([], [])

    def test_working_datetime_ranges_of_date_empty(self):
        d = date(year=1993, month=9, day=26)
        self.assertEqual(working_datetime_ranges_of_date(d, {}, {}, True), [])
        self.assertEqual(working_datetime_ranges_of_date(d, {}, {}, False), [])

    def test_working_datetime_ranges_of_date(self):
        d = date(year=1993, month=9, day=26)
        swh = {
            d: [
                (time(hour=9), time(hour=12)),
                (time(hour=21), time(hour=0)),
            ]
        }
        expected_r = [
            (
                datetime(year=1993, month=9, day=26, hour=9),
                datetime(year=1993, month=9, day=26, hour=12),
            ),
            (
                datetime(year=1993, month=9, day=26, hour=21),
                datetime(year=1993, month=9, day=27, hour=0),
            )
        ]
        self.assertEqual(working_datetime_ranges_of_date(d, swh, {}, True),
                         expected_r)
        self.assertEqual(working_datetime_ranges_of_date(d, swh, {}, False),
                         expected_r)

    def test_working_datetime_ranges_of_date_merging_tomorrow(self):
        d = date(year=1993, month=9, day=26)
        swh = {
            d: [
                (time(hour=9), time(hour=12)),
                (time(hour=21), time(hour=0)),
            ]
        }
        wwh_contiguous = {
            tomorrow(d).weekday(): [
                (time(hour=0), time(hour=12))
            ]
        }
        wwh_separated = {
            tomorrow(d).weekday(): [
                (time(hour=1), time(hour=12))
            ]
        }

        r_s = working_datetime_ranges_of_date(d, swh, wwh_separated,
                                              merge_tomorrow=False)
        r_s_merged = working_datetime_ranges_of_date(d, swh, wwh_separated,
                                                     merge_tomorrow=True)
        r_c = working_datetime_ranges_of_date(d, swh, wwh_contiguous,
                                              merge_tomorrow=False)
        r_c_merged = working_datetime_ranges_of_date(d, swh, wwh_contiguous,
                                                     merge_tomorrow=True)
        expected_r_only_today = [
            (
                datetime(year=1993, month=9, day=26, hour=9),
                datetime(year=1993, month=9, day=26, hour=12),
            ),
            (
                datetime(year=1993, month=9, day=26, hour=21),
                datetime(year=1993, month=9, day=27, hour=0),
            )
        ]
        expected_r_with_tomorrow = [
            (
                datetime(year=1993, month=9, day=26, hour=9),
                datetime(year=1993, month=9, day=26, hour=12),
            ),
            (
                datetime(year=1993, month=9, day=26, hour=21),
                datetime(year=1993, month=9, day=27, hour=12),
            )
        ]

        self.assertEqual(r_s, expected_r_only_today)
        self.assertEqual(r_s_merged, expected_r_only_today)
        self.assertEqual(r_c, expected_r_only_today)
        self.assertEqual(r_c_merged, expected_r_with_tomorrow)
