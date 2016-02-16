import unittest
import fixtures
from datetime import timedelta
from booking_engine.engine import (
    calculate_ranges, get_service_step, get_service_duration
)


class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_service_step(self):
        self.assertEquals(
            get_service_step(fixtures.galactic_service_recipe),
            timedelta(minutes=5))

    def test_get_service_duration(self):
        self.assertEquals(
            get_service_duration(fixtures.galactic_service_recipe),
            timedelta(hours=1, minutes=30))

    def test_wrong_period(self):
        self.assertRaises(ValueError, calculate_ranges, fixtures.wrong_period,
                          fixtures.availability, fixtures.service_recipe,
                          fixtures.resources)

    def test_calculate_ranges(self):
        ranges = calculate_ranges(fixtures.period,
                                  fixtures.availability,
                                  fixtures.service_recipe, fixtures.resources)

        self.assertEquals(ranges[0], fixtures.expected_ranges[0])
