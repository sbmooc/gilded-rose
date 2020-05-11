import operator
from math import inf
from typing import Union, List


class QualityChange:
    def __init__(
        self,
        min_sell_by: Union[int, float],
        max_sell_by: Union[int, float],
        quality_change=None,
        set_quality=None,
    ):
        self.min_sell_by = min_sell_by
        self.max_sell_by = max_sell_by
        self.set_quality = set_quality
        self.quality_change = quality_change


class ItemRulesNotValid(BaseException):
    pass


class ItemRules:
    def __init__(
        self, quality_change_rules: List[QualityChange], sell_by_rate_decrease: int
    ):
        self.quality_change_rules = quality_change_rules
        self.sell_by_rate_decrease = sell_by_rate_decrease
        self._sort_and_validate_rules()

    def _sort_and_validate_rules(self):
        self.quality_change_rules.sort(key=operator.attrgetter("min_sell_by"))
        if (
            self.quality_change_rules[0].min_sell_by != -inf
            or self.quality_change_rules[-1].max_sell_by != inf
        ):
            raise ItemRulesNotValid
        for index, rule in enumerate(self.quality_change_rules[:-1]):
            if rule.max_sell_by != self.quality_change_rules[index + 1].min_sell_by:
                raise ItemRulesNotValid


specific_item_rules = {
    "Aged Brie": ItemRules(
        [
            QualityChange(-inf, 0, quality_change=2),
            QualityChange(0, inf, quality_change=1),
        ],
        1,
    ),
    "Sulfuras, Hand of Ragnaros": ItemRules(
        [QualityChange(-inf, inf, quality_change=0)], 0
    ),
    "Conjured Item": ItemRules(
        [
            QualityChange(-inf, 0, quality_change=-4),
            QualityChange(0, inf, quality_change=-2),
        ],
        1,
    ),
    "Backstage passes to a TAFKAL80ETC concert": ItemRules(
        [
            QualityChange(-inf, 0, 0, set_quality=0),
            QualityChange(0, 5, quality_change=3),
            QualityChange(5, 10, quality_change=2),
            QualityChange(10, inf, quality_change=1),
        ],
        1,
    ),
}
generic_item_rules = ItemRules(
    [
        QualityChange(-inf, 0, quality_change=-2),
        QualityChange(0, inf, quality_change=-1),
    ],
    1,
)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRose:
    def __init__(self, items: List[Item]):
        self.items = items
        self.quality_never_below = 0
        self.quality_never_above = 50

    @staticmethod
    def _update_item_sell_by_rate(item):
        return item.sell_in - item.ruleset.sell_by_rate_decrease

    @staticmethod
    def _get_item_ruleset(item):
        try:
            return specific_item_rules[item.name]
        except KeyError:
            return generic_item_rules

    @staticmethod
    def _find_quality_change_rule(sell_in, ruleset):
        for rule in ruleset:
            if rule.min_sell_by <= sell_in < rule.max_sell_by:
                return rule

    def _ensure_quality_within_bounds(self, quality):
        if quality <= self.quality_never_below:
            return self.quality_never_below
        elif quality >= self.quality_never_above:
            return self.quality_never_above
        return quality

    def _update_item_quality(self, item):
        quality_change_rule = self._find_quality_change_rule(
            item.sell_in, item.ruleset.quality_change_rules
        )
        if quality_change_rule.set_quality is not None:
            return quality_change_rule.set_quality
        new_quality = item.quality + quality_change_rule.quality_change
        return self._ensure_quality_within_bounds(new_quality)

    def update_quality(self):
        for item in self.items:
            item.ruleset = self._get_item_ruleset(item)
            item.sell_in = self._update_item_sell_by_rate(item)
            item.quality = self._update_item_quality(item)
