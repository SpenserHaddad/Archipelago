from __future__ import annotations

from Options import AssembleOptions, Range

from .Constants import (
    MAX_LEGENDARY_CRATE_DROPS,
    MAX_NORMAL_CRATE_DROPS,
    MAX_SHOP_LOCATIONS_PER_TIER,
    NUM_CHARACTERS,
    NUM_WAVES,
    ItemRarity,
)

# TODO: Location every x run wins (0-20)


# class AllowRepeatCharacterVictories(Toggle):
#     """
#     If set, then you can win runs with the same character multiple times to progress.

#     Otherwise, run wins must be done with unique characters.
#     """

#     default = False
#     display_name = "Character Unique Run Wins"


# class NumberRequiredVictoriesWithRepeat(Range):
#     """
#     The number of run wins required for Victory if allowed to reuse characters.
#     """

#     range_start = 1
#     range_end = MAX_REQUIRED_RUN_WINS

#     display_name = "Number of Victories (Repeats Allowed)"
#     default = 10


# class NumberRequiredWinsUniqueCharacters(Range):

#     """
#     The number of run wins required for Victory if runs must be won with different
#     characters.
#     """

#     range_start = 1
#     range_end = NUM_CHARACTERS

#     display_name = "Number of Victories (Unique Characters)"
#     default = 10


class NumberRequiredWins(Range):
    """The number of characters you must complete runs with to win."""

    range_start = 1
    range_end = NUM_CHARACTERS

    display_name = "Number of runs required"
    default = 10


class WavesPerCheck(Range):
    """How many waves to win to receive a check. Smaller values mean more frequent checks."""

    range_start = 1
    range_end = NUM_WAVES

    display_name = "Waves per check"
    default = 10


class NumberCrateDropLocations(Range):
    """
    The first <count> normal crate drops will be AP locations.
    """

    range_start = 0
    range_end = MAX_NORMAL_CRATE_DROPS

    display_name = "Number of normal crate drop locations"
    default = 25


class NumberLegendaryCrateDropLocations(Range):
    """
    The first <count> legendary crate drops will be AP locations.
    """

    range_start = 0
    range_end = MAX_LEGENDARY_CRATE_DROPS

    display_name = "Number of legendary crate drop locations"
    default = 5


class NumberShopItems(Range):
    """The number of items to place in the shop"""

    range_start = 0
    range_end = MAX_SHOP_LOCATIONS_PER_TIER[ItemRarity.COMMON]
    display_name = "Shop items"
    default = 10


options: dict[str, AssembleOptions] = {
    # "allow_repeat_characters": AllowRepeatCharacterVictories,
    # "num_repeat_victories": NumberRequiredVictoriesWithRepeat,
    # "num_unique_victories": NumberRequiredWinsUniqueCharacters,
    "num_victories": NumberRequiredWins,
    "waves_per_drop": WavesPerCheck,
    "num_common_crate_drops": NumberCrateDropLocations,
    "num_legendary_crate_drops": NumberLegendaryCrateDropLocations,
    "num_shop_items": NumberShopItems,
}
