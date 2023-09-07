from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from .Constants import BASE_ID


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


# _locations = [
#     BrotatoLocation(name="Wave 1"),
#     BrotatoLocation(name="Wave 2"),
#     BrotatoLocation(name="Wave 3"),
#     BrotatoLocation(name="Wave 4"),
#     BrotatoLocation(name="Wave 5"),
#     BrotatoLocation(name="Wave 6"),
#     BrotatoLocation(name="Wave 7"),
#     BrotatoLocation(name="Wave 8"),
#     BrotatoLocation(name="Wave 9"),
#     BrotatoLocation(name="Wave 10"),
#     BrotatoLocation(name="Wave 11"),
#     BrotatoLocation(name="Wave 12"),
#     BrotatoLocation(name="Wave 13"),
#     BrotatoLocation(name="Wave 14"),
#     BrotatoLocation(name="Wave 15"),
#     BrotatoLocation(name="Wave 16"),
#     BrotatoLocation(name="Wave 17"),
#     BrotatoLocation(name="Wave 18"),
#     BrotatoLocation(name="Wave 19"),
#     BrotatoLocation(name="Wave 20"),
#     BrotatoLocation(name="Run Complete", is_event=True),
# ]

location_table: list[BrotatoLocation] = [
    *[BrotatoLocation(name=f"Common Pickup {i}") for i in range(25)],
    *[BrotatoLocation(name=f"Uncommon Pickup {i}") for i in range(10)],
    *[BrotatoLocation(name=f"Rare Pickup {i}") for i in range(10)],
    *[BrotatoLocation(name=f"Legendary Pickup {i}") for i in range(10)],
    *[BrotatoLocation(name=f"Shop Item {i}") for i in range(10)],
]
