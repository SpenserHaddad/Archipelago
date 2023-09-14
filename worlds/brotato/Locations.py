from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import ClassVar

from .Constants import (
    BASE_ID,
    CHARACTERS,
    MAX_LEGENDARY_CRATE_DROPS,
    MAX_NORMAL_CRATE_DROPS,
    MAX_REQUIRED_RUN_WINS,
    MAX_SHOP_LOCATIONS_PER_TIER,
    NUM_WAVES,
)


# TODO: Subclass base Location
@dataclass(frozen=True)
class BrotatoLocation:
    name: str
    is_event: bool = False
    id: int = field(init=False)
    _next_offset: ClassVar[int] = 0

    def __post_init__(self):
        if not self.is_event:
            id_ = BASE_ID + BrotatoLocation._next_offset
            BrotatoLocation._next_offset += 1
        else:
            id_ = None
        object.__setattr__(self, "id", id_)


_wave_count = range(NUM_WAVES)
_run_count = range(MAX_REQUIRED_RUN_WINS)

_char_generic_wave_complete_locs = [
    BrotatoLocation(name=f"Run {r} - Wave {w} Complete") for w, r in product(_wave_count, _run_count)
]
_char_specific_wave_complete_locs = [
    BrotatoLocation(name=f"Wave {w} Complete ({char})") for w, char in product(_wave_count, CHARACTERS)
]
_char_generic_run_complete_locs = [BrotatoLocation(name=f"Run {r} Complete") for r in range(MAX_REQUIRED_RUN_WINS)]
_char_specific_run_complete_locs = [BrotatoLocation(name=f"Run Complete ({char})") for char in CHARACTERS]
_shop_item_locs = []
for tier, max_shop_locs in MAX_SHOP_LOCATIONS_PER_TIER.items():
    _shop_item_locs += [BrotatoLocation(name=f"{tier.name} Shop Item {i}") for i in range(max_shop_locs)]

_normal_item_drop_locs = [BrotatoLocation(name=f"Crate Drop {i}") for i in range(MAX_NORMAL_CRATE_DROPS)]
_legendary_item_drop_locs = [
    BrotatoLocation(name=f"Legendary Crate Drop {i}") for i in range(MAX_LEGENDARY_CRATE_DROPS)
]

location_table: list[BrotatoLocation] = [
    *_char_generic_wave_complete_locs,
    *_char_specific_wave_complete_locs,
    *_char_generic_run_complete_locs,
    *_char_specific_run_complete_locs,
    *_shop_item_locs,
    *_normal_item_drop_locs,
    *_legendary_item_drop_locs,
]

location_id_to_name: dict[int, str] = {loc.id: loc.name for loc in location_table}
location_name_to_id: dict[str, int] = {v: k for k, v in location_id_to_name.items()}
