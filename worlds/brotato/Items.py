from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from BaseClasses import Item, ItemClassification

from .Constants import BASE_ID


@dataclass(frozen=True)
class BrotatoItemBase:
    name: ItemName
    classification: ItemClassification
    code: int = field(init=False)
    _next_offset: ClassVar[int] = 0

    def __post_init__(self):
        object.__setattr__(self, "code", BASE_ID + BrotatoItemBase._next_offset)
        BrotatoItemBase._next_offset += 1


class BrotatoItem(Item):
    game = "Brotato"

    @staticmethod
    def from_item_base(base: BrotatoItemBase, player: int):
        return BrotatoItem(base.name.value, base.classification, base.code, player)


class ItemName(Enum):
    COMMON_ITEM = "Common Item"
    UNCOMMON_ITEM = "Uncommon Item"
    RARE_ITEM = "Rare Item"
    LEGENDARY_ITEM = "Legendary Item"
    XP_5 = "XP (5)"
    XP_10 = "XP (10)"
    XP_25 = "XP (25)"
    XP_50 = "XP (50)"
    XP_100 = "XP (100)"
    XP_150 = "XP (150)"
    GOLD_10 = "Gold (10)"
    GOLD_25 = "Gold (25)"
    GOLD_50 = "Gold (50)"
    GOLD_100 = "Gold (100)"
    GOLD_200 = "Gold (200)"
    PROGRESSIVE_CHARACTER = "Progressive Character"
    RUN_COMPLETE = "Run Complete"


_items: list[BrotatoItemBase] = [
    BrotatoItemBase(name=ItemName.COMMON_ITEM, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.UNCOMMON_ITEM, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.RARE_ITEM, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.LEGENDARY_ITEM, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_5, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_10, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_25, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_50, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_100, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_150, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_10, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_25, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_50, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_100, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_200, classification=ItemClassification.filler),
    BrotatoItemBase(
        name=ItemName.PROGRESSIVE_CHARACTER,
        classification=ItemClassification.progression,
    ),
    BrotatoItemBase(name=ItemName.RUN_COMPLETE, classification=ItemClassification.progression),
]

item_table = {item.code: item for item in _items}

item_name_groups = {
    "Item Drops": {
        ItemName.COMMON_ITEM.value,
        ItemName.UNCOMMON_ITEM.value,
        ItemName.RARE_ITEM.value,
        ItemName.LEGENDARY_ITEM.value,
    },
    "Gold and XP": {
        ItemName.XP_5.value,
        ItemName.XP_10.value,
        ItemName.XP_25.value,
        ItemName.XP_50.value,
        ItemName.XP_100.value,
        ItemName.XP_150.value,
        ItemName.GOLD_10.value,
        ItemName.GOLD_25.value,
        ItemName.GOLD_50.value,
        ItemName.GOLD_100.value,
        ItemName.GOLD_200.value,
    },
    "Characters": {ItemName.PROGRESSIVE_CHARACTER.value},
}
