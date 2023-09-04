from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

_BASE_ID = 200_000


@dataclass(frozen=True)
class BrotatoLocation:
    name: str
    id: int = field(init=False)
    _next_offset: ClassVar[int] = 0

    def __post_init__(self):
        object.__setattr__(self, "id", _BASE_ID + BrotatoLocation._next_offset)
        BrotatoLocation._next_offset += 1


location_table: list[BrotatoLocation] = [
    *[BrotatoLocation(name=f"Common Pickup {i}") for i in range(25)],
    *[BrotatoLocation(name=f"Uncommon Pickup {i}") for i in range(10)],
    *[BrotatoLocation(name=f"Rare Pickup {i}") for i in range(10)],
    *[BrotatoLocation(name=f"Legendary Pickup {i}") for i in range(10)],
]
