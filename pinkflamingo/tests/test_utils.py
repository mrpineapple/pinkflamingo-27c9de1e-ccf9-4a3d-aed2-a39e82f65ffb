# encoding: utf-8
from __future__ import unicode_literals

from django.test import TestCase
from nose.tools import assert_equal, assert_raises
from pinkflamingo import utils


class TestRounding(TestCase):

    def test_round_to_half_whole_number(self):
        """Rounding a whole number should return that number"""
        expected = 2.0
        assert_equal(expected, utils.round_to_ratings_half(2))
        assert_equal(expected, utils.round_to_ratings_half(2.0))

    def test_round_to_half_negative_fails(self):
        """Rounding a negative number raises a ValueError"""
        with assert_raises(ValueError):
            utils.round_to_ratings_half(-2.5)

    def test_round_to_half_bogus_input_fails(self):
        """Rounding something other than int or float raises a ValueError"""

        with assert_raises(ValueError):
            utils.round_to_ratings_half(False)

        with assert_raises(ValueError):
            utils.round_to_ratings_half(True)

        with assert_raises(ValueError):
            utils.round_to_ratings_half('Foobar')

    def test_round_to_half_none(self):
        """Rounding None or zero should return zero"""
        expected = 0.0
        assert_equal(expected, utils.round_to_ratings_half(None))
        assert_equal(expected, utils.round_to_ratings_half(0.0))

    def test_round_to_ratings_half_down(self):
        """Rounding something between .0 and .2 should round down"""
        expected = 2.0
        assert_equal(expected, utils.round_to_ratings_half(2.1))
        assert_equal(expected, utils.round_to_ratings_half(2.2))

    def test_round_to_ratings_half_up(self):
        """Rounding something between .8 and .9 should round up"""
        expected = 3.0
        assert_equal(expected, utils.round_to_ratings_half(2.8))
        assert_equal(expected, utils.round_to_ratings_half(2.9))

    def test_round_to_ratings_half_to_point_five(self):
        """Rounding something between .3 and .7 should round to .5"""
        expected = 2.5
        assert_equal(expected, utils.round_to_ratings_half(2.3))
        assert_equal(expected, utils.round_to_ratings_half(2.4))
        assert_equal(expected, utils.round_to_ratings_half(2.5))
        assert_equal(expected, utils.round_to_ratings_half(2.6))
        assert_equal(expected, utils.round_to_ratings_half(2.7))

    def test_round_to_ratings_with_extra_precision(self):
        """Rounding something more than tenths precision should round first, then process"""
        expected = 3.0
        assert_equal(expected, utils.round_to_ratings_half(2.777))
        expected = 2.5
        assert_equal(expected, utils.round_to_ratings_half(2.699))
        expected = 2.5
        assert_equal(expected, utils.round_to_ratings_half(2.299))
        expected = 2.0
        assert_equal(expected, utils.round_to_ratings_half(2.199))
