from math import inf

NORMAL_QUALITY_CHANGE = 1
QUALITY_NEVER_ABOVE = 50
QUALITY_NEVER_BELOW = 0


class ItemRules:

    def __init__(
            self,
            quality_change_rules,
            sell_by_rate_decrease: int
    ):
        self.quality_change_rules = quality_change_rules
        self.sell_by_rate_decrease = sell_by_rate_decrease


class QualityChange:

    def __init__(
            self,
            min_sell_by,
            max_sell_by,
            quality_change_rate,
            set_quality=None
    ):
        self.min_sell_by = min_sell_by
        self.max_sell_by = max_sell_by
        self.quality_change_rate = quality_change_rate
        self.set_quality = set_quality


specific_item_rules = {
    'Aged Brie': ItemRules({QualityChange(-inf, 0, 2), QualityChange(0, inf, 1)}, 1),
    'Sulfuras, Hand of Ragnaros': ItemRules({QualityChange(-inf, inf, 0)}, 0),
    'Conjured Item': ItemRules({QualityChange(-inf, 0, -4), QualityChange(0, inf, -2)}, 1),
    'Backstage passes to a TAFKAL80ETC concert': ItemRules(
        {
            QualityChange(-inf, 0, 0, set_quality=0),
            QualityChange(0, 5, 3),
            QualityChange(5, 10, 2),
            QualityChange(10, inf, 1)
        },
        1
    )
}
generic_item_rules = ItemRules({QualityChange(-inf, 0, -2), QualityChange(0, inf, -1)}, 1)


class MultipleRuleSetsForSellByDateError(BaseException):
    pass


class GildedRose:

    def __init__(self, items):
        self.items = items

    def _reduce_sell_by_rate(self, item):
        return item.sell_in - item.ruleset.sell_by_rate_decrease

    def _get_item_ruleset(self, item):
        try:
            return specific_item_rules[item.name]
        except KeyError:
            return generic_item_rules

    def _find_quality_change_rule(self, sell_in, ruleset):
        matched_rulesets = []
        for rule in ruleset:
            if rule.min_sell_by < sell_in <= rule.max_sell_by:
                matched_rulesets.append(rule)
        if len(matched_rulesets) > 1:
            raise MultipleRuleSetsForSellByDateError
        if len(matched_rulesets) == 0:
            raise MultipleRuleSetsForSellByDateError
        return matched_rulesets[0]

    def _update_item_quality(self, item, quality_never_below, quality_never_above):
        quality_change_rule = self._find_quality_change_rule(item.sell_in, item.ruleset.quality_change_rules)
        if quality_change_rule.set_quality is not None:
            return quality_change_rule.set_quality
        new_quality = item.quality + (NORMAL_QUALITY_CHANGE * quality_change_rule.quality_change_rate)
        if new_quality <= quality_never_below:
            return quality_never_below
        elif new_quality >= quality_never_above:
            return quality_never_above
        return new_quality

    def update_quality(self):
        for item in self.items:
            item.ruleset = self._get_item_ruleset(item)
            item.sell_in = self._reduce_sell_by_rate(item)
            item.quality = self._update_item_quality(item, QUALITY_NEVER_BELOW, QUALITY_NEVER_ABOVE)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
