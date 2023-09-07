import typing

from Options import AssembleOptions, Range


class NumberVictories(Range):
    """
    The number of run wins required for Victory.
    """

    range_start = 0
    range_end = 44

    display_name = "Number of Victories"
    default = 10


class NumberCommonItems(Range):
    """
    The number of common item drops to include in the pool.
    """

    range_start = 0
    range_end = 30
    default = 25
    display_name = "Number of Common Items"


class NumberUncommonItems(Range):
    """
    The number of uncommon item drops to include in the pool.
    """

    range_start = 0
    range_end = 30
    default = 25
    display_name = "Number of Uncommon Items"


class NumberRareItems(Range):
    """
    The number of rare item drops to include in the pool.
    """

    range_start = 0
    range_end = 30
    default = 5
    display_name = "Number of Rare Items"


class NumberLegendaryItems(Range):
    """
    The number of legendary item drops to include in the pool.
    """

    range_start = 0
    range_end = 30
    default = 2
    display_name = "Number of Legendary Items"


options: typing.Dict[str, AssembleOptions] = {
    "num_victories": NumberVictories,
    "num_common_items": NumberCommonItems,
    "num_uncommon_items": NumberUncommonItems,
    "num_rare_items": NumberRareItems,
    "num_legendary_items": NumberLegendaryItems,
}
