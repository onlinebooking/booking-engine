import unittest
from booking_engine import engine
import fixtures

class TestEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_wrong_period(self):
        self.assertRaises(ValueError, engine.calculate_ranges, fixtures.wrong_period, 
            fixtures.availability, fixtures.service_recipe, fixtures.resources)
        
    def test_calculate_ranges(self):
        #TODO: infinite loop....
        return
        ranges = engine.calculate_ranges(fixtures.period, 
            fixtures.availability, fixtures.service_recipe, fixtures.resources)