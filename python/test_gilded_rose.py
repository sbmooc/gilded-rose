# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class TestAgedBrie(unittest.TestCase):

    def setUp(self):
        self.aged_brie = Item('Aged Brie', None, None)

    def test_aged_brie_increases_in_quality_prior_to_sell_by_date(self):
        self.aged_brie.quality = 0
        self.aged_brie.sell_in = 10
        gilded_rose = GildedRose([self.aged_brie, ])
        gilded_rose.update_quality()
        assert self.aged_brie.quality == 1

    def test_aged_brie_increases_faster_past_sell_by_date(self):
        self.aged_brie.quality = 0
        self.aged_brie.sell_in = 0
        gilded_rose = GildedRose([self.aged_brie, ])
        gilded_rose.update_quality()
        assert self.aged_brie.quality == 2

    def test_aged_brie_cannot_have_greater_than_50_quality(self):
        self.aged_brie.quality = 50
        self.aged_brie.sell_in = 10
        gilded_rose = GildedRose([self.aged_brie, ])
        gilded_rose.update_quality()
        assert self.aged_brie.quality == 50


class TestSulfuras(unittest.TestCase):
    pass

class TestGenericItems(unittest.TestCase):

    def setUp(self):
        self.generic_item = Item('Test Item', 10, 10)
        self.gilded_rose = GildedRose([self.generic_item, ])

    def test_sell_in_day_and_quality_decreases_by_one(self):
        self.gilded_rose.update_quality()
        assert self.generic_item.sell_in == 9
        assert self.generic_item.quality == 9

    def test_quality_can_not_be_negative(self):
        self.generic_item.quality = 0
        self.gilded_rose.update_quality()
        assert self.generic_item.quality == 0

    def test_quality_degrades_twice_as_fast_after_sell_in_date(self):
        self.generic_item.quality = 4
        self.generic_item.sell_in = 0
        self.gilded_rose.update_quality()
        assert self.generic_item.quality == 2
        assert self.generic_item.sell_in == -1


if __name__ == '__main__':
    unittest.main()
