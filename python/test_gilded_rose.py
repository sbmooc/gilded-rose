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
        self.aged_brie.quality = 49
        self.aged_brie.sell_in = -2
        gilded_rose = GildedRose([self.aged_brie, ])
        gilded_rose.update_quality()
        assert self.aged_brie.quality == 50


class TestSulfuras(unittest.TestCase):

    def setUp(self):
        self.sulfuras = Item('Sulfuras, Hand of Ragnaros', 10, 10)
        self.gilded_rose = GildedRose([self.sulfuras, ])

    def test_sulfuras_never_drop_in_quality_or_need_to_be_sold(self):
        self.gilded_rose.update_quality()
        assert self.sulfuras.sell_in == 10
        assert self.sulfuras.quality == 10


class TestBackStagePasses(unittest.TestCase):

    def setUp(self):
        self.backstage_pass = Item('Backstage passes to a TAFKAL80ETC concert', 0, 0)
        self.gilded_rose = GildedRose([self.backstage_pass, ])

    def test_back_stage_passes_increase_in_quality_at_normal_rate(self):
        self.backstage_pass.sell_in = 11
        self.backstage_pass.quality = 10
        self.gilded_rose.update_quality()
        assert self.backstage_pass.quality == 11

    def test_back_stage_passes_increase_in_quality_at_faster_rate_close_to_concert(self):
        self.backstage_pass.sell_in = 10
        self.backstage_pass.quality = 10
        self.gilded_rose.update_quality()
        assert self.backstage_pass.quality == 12
        self.backstage_pass.sell_in = 5
        self.backstage_pass.quality = 5
        self.gilded_rose.update_quality()
        assert self.backstage_pass.quality == 8

    def test_back_stage_passes_have_zero_quality_after_concert(self):
        self.backstage_pass.sell_in = 0
        self.backstage_pass.quality = 10
        self.gilded_rose.update_quality()
        assert self.backstage_pass.quality == 0

    def test_back_stage_passes_quality_does_not_exceed_50(self):
        self.backstage_pass.sell_in = 2
        self.backstage_pass.quality = 49
        self.gilded_rose.update_quality()
        assert self.backstage_pass.quality == 50


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
