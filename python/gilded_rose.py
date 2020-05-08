from math import inf

QUALITY_NEVER_ABOVE = 50
QUALITY_NEVER_BELOW = 0


class ItemRules:
    def __init__(self, quality_change_rules, sell_by_rate_decrease: int):
        self.quality_change_rules = quality_change_rules
        self.sell_by_rate_decrease = sell_by_rate_decrease


class QualityChange:
    def __init__(
        self,
        min_sell_by,
        max_sell_by,
        quality_change_rate=None,
        quality_change=None,
        set_quality=None,
    ):
        self.min_sell_by = min_sell_by
        self.max_sell_by = max_sell_by
        self.quality_change_rate = quality_change_rate
        self.set_quality = set_quality
        self.quality_change = quality_change


specific_item_rules = {
    "Aged Brie": ItemRules(
        {
            QualityChange(-inf, 0, quality_change=2),
            QualityChange(0, inf, quality_change=1),
        },
        1,
    ),
    "Sulfuras, Hand of Ragnaros": ItemRules(
        {QualityChange(-inf, inf, quality_change=0)}, 0
    ),
    "Conjured Item": ItemRules(
        {
            QualityChange(-inf, 0, quality_change=-4),
            QualityChange(0, inf, quality_change=-2),
        },
        1,
    ),
    "Backstage passes to a TAFKAL80ETC concert": ItemRules(
        {
            QualityChange(-inf, 0, 0, set_quality=0),
            QualityChange(0, 5, quality_change=3),
            QualityChange(5, 10, quality_change=2),
            QualityChange(10, inf, quality_change=1),
        },
        1,
    ),
}
generic_item_rules = ItemRules(
    {
        QualityChange(-inf, 0, quality_change=-2),
        QualityChange(0, inf, quality_change=-1),
    },
    1,
)


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
            if rule.min_sell_by <= sell_in < rule.max_sell_by:
                matched_rulesets.append(rule)
        return matched_rulesets[0]

    def _ensure_quality_within_bounds(self, quality, quality_never_below, quality_never_above):
        if quality <= quality_never_below:
            return quality_never_below
        elif quality >= quality_never_above:
            return quality_never_above
        return quality

    def _update_item_quality(self, item, quality_never_below, quality_never_above):
        quality_change_rule = self._find_quality_change_rule(
            item.sell_in, item.ruleset.quality_change_rules
        )
        if quality_change_rule.set_quality is not None:
            return quality_change_rule.set_quality
        new_quality = item.quality + quality_change_rule.quality_change
        return self._ensure_quality_within_bounds(new_quality, quality_never_below, quality_never_above)

    def update_quality(self):
        for item in self.items:
            item.ruleset = self._get_item_ruleset(item)
            item.sell_in = self._reduce_sell_by_rate(item)
            item.quality = self._update_item_quality(
                item, QUALITY_NEVER_BELOW, QUALITY_NEVER_ABOVE
            )


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
