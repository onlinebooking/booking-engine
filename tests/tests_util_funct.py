import unittest
from booking_engine.util.funct import (
    any_match, first_match,
)


def stupid_predicate(n):
    """
    A stupid function for test purpose only, check if given number is
    grater then 10
    """
    return n > 10


class TestFunctUtil(unittest.TestCase):

    def setUp(self):
        pass

    def test_any_match_that_match(self):
        assert any_match(stupid_predicate, [1, 2, 3, 11, 1, 5, 6])

    def test_any_match_that_not_match(self):
        assert not any_match(stupid_predicate, [1, 2, 3, -11, 1, 5, 6])

    def test_any_match_with_none(self):
        assert any_match(None, [False, 0, None, -1])
        assert not any_match(None, [False, 0, None, ''])

    def test_first_match_to_be_first(self):
        self.assertEqual(first_match(stupid_predicate, xrange(0, 100)), 11)

    def test_first_match_not_match(self):
        self.assertEqual(first_match(stupid_predicate, xrange(0, 10)), None)

    def test_first_match_with_none(self):
        self.assertEqual(first_match(None, [None, 0, -99, '']), -99)
