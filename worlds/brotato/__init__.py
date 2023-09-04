import logging
from typing import List

from BaseClasses import Item, Location, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import Items, Locations, Options

logger = logging.getLogger("Brotato")


class BrotatoLocation(Location):
    game: str = "Brotato"


class BrotatoItem(Item):
    game: str = "Brotato"


class BrotatoWeb(WebWorld):
    # TODO: Add actual tutorial!
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Brotato randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["RampagingHippy"],
        )
    ]
    theme = "dirt"


class BrotatoWorld(World):
    """
    Brotato is a top-down arena shooter roguelite where you play a potato wielding up to
    6 weapons at a time to fight off hordes of aliens. Choose from a variety of traits
    and items to create unique builds and survive until help arrives.
    """

    option_definitions = Options.options
    game = "Brotato"
    web = BrotatoWeb()
    data_version = 3
    required_client_version = (0, 4, 2)

    item_name_to_id = {item.id: item for item in Items.item_table}
    item_name_groups = Items.item_name_groups

    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    location_name_groups = Locations.location_name_groups

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def generate_early(self):
        pass

    def set_rules(self):
        pass

    def create_item(self, name: str) -> BrotatoItem:
        item_id: int = self.item_name_to_id[name]
        return BrotatoItem(name, Items.item_table[item_id]["classification"], item_id, self.player)

    def create_items(self):
        itempool: List[BrotatoItem] = []
        self.multiworld.itempool += itempool

    def get_filler_item_name(self):
        return self.multiworld.random.choice(
            [
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
            ]
        )
