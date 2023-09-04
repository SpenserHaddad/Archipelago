from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from BaseClasses import Item, ItemClassification

_BASE_ID = 200_000

_CHARACTERS = [
    "Well Rounded",
    "Brawler",
    "Crazy"
    "Ranger"
    "Mage"
    "Chunky"
    "Old"
    "Lucky"
    "Mutant"
    "Generalist"
    "Loud"
    "Multitasker"
    "Wildling"
    "Pacifist"
    "Gladiator"
    "Saver"
    "Sick"
    "Farmer"
    "Ghost"
    "Speedy"
    "Entrepeneur"
    "Engineer"
    "Explorer"
    "Doctor"
    "Hunter"
    "Artificer"
    "Arms Dealer"
    "Streamer"
    "Cyborg"
    "Glutton"
    "Jack"
    "Lich"
    "Appentice"
    "Cryptid"
    "Fisherman"
    "Golem"
    "King"
    "Renegade"
    "One Armed"
    "Bull"
    "Soldier"
    "Masochist"
    "Knight"
    "Demon",
]

_DEFAULT_CHARACTERS = ["Well Rounded", "Brawler", "Crazy" "Ranger" "Mage"]


@dataclass(frozen=True)
class BrotatoItem(Item):
    game = "Brotato"
    name: str
    classification: ItemClassification
    count: int = 1
    id: int = field(init=False)
    _next_offset: ClassVar[int] = 0

    def __post_init__(self):
        object.__setattr__(self, "id", _BASE_ID + BrotatoItem._next_offset)
        BrotatoItem._next_offset += 1


item_table: list[BrotatoItem] = [
    BrotatoItem(name="Common Item", classification=ItemClassification.filler, count=25),
    BrotatoItem(name="Uncommon Item", classification=ItemClassification.filler, count=10),
    BrotatoItem(name="Rare Item", classification=ItemClassification.filler, count=5),
    BrotatoItem(name="Legendary Item", classification=ItemClassification.filler, count=3),
    BrotatoItem(name="XP (5)", classification=ItemClassification.filler, count=40),
    BrotatoItem(name="XP (10)", classification=ItemClassification.filler, count=30),
    BrotatoItem(name="XP (25)", classification=ItemClassification.filler, count=25),
    BrotatoItem(name="XP (50)", classification=ItemClassification.filler, count=15),
    BrotatoItem(name="XP (100)", classification=ItemClassification.filler, count=15),
    BrotatoItem(name="XP (150)", classification=ItemClassification.filler, count=15),
    BrotatoItem(name="Gold (10)", classification=ItemClassification.filler, count=30),
    BrotatoItem(name="Gold (25)", classification=ItemClassification.filler, count=25),
    BrotatoItem(name="Gold (50)", classification=ItemClassification.filler, count=15),
    BrotatoItem(name="Gold (100)", classification=ItemClassification.filler, count=15),
    BrotatoItem(name="Gold (200)", classification=ItemClassification.filler, count=15),
    BrotatoItem(
        name="Progressive Character",
        classification=ItemClassification.progression,
        count=len(_CHARACTERS) - len(_DEFAULT_CHARACTERS),
    ),
]

item_name_groups = {
    "Item Drops": ["Common Item", "Uncommon Item", "Rare Item", "Legendary Item"],
    "Money and XP": [
        "XP (5)",
        "XP (10)",
        "XP (25)",
        "XP (50)",
        "XP (100)",
        "XP (150)",
        "Gold (10)",
        "Gold (25)",
        "Gold (50)",
        "Gold (100)",
        "Gold (200)",
    ],
    "Characters": ["Progressive Character"],
}
