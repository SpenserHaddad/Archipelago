import logging

from BaseClasses import ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import Options
from .Items import BrotatoItem, item_name_groups, item_table, ItemName
from .Locations import location_table
from .Regions import create_regions

logger = logging.getLogger("Brotato")


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

    item_name_to_id = {item.name.value: code for code, item in item_table.items()}
    item_name_groups = item_name_groups

    _filler_items = [
        item.name.value for item in item_table.values() if item.classification == ItemClassification.filler
    ]

    location_name_to_id = {loc.name: loc.id for loc in location_table}
    # location_name_groups = location_name_groups

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def generate_early(self):
        pass

    def set_rules(self):
        pass

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def create_item(self, name: str | ItemName) -> BrotatoItem:
        if isinstance(name, ItemName):
            name = name.value
        return BrotatoItem.from_item_base(item_table[self.item_name_to_id[name]], self.player)

    def create_items(self):
        item_names: list[ItemName] = []

        for _ in range(39):
            item_names.append(ItemName.PROGRESSIVE_CHARACTER)

        for _ in range(self.multiworld.num_common_items[self.player]):
            item_names.append(ItemName.COMMON_ITEM)

        for _ in range(self.multiworld.num_uncommon_items[self.player]):
            item_names.append(ItemName.UNCOMMON_ITEM)

        for _ in range(self.multiworld.num_rare_items[self.player]):
            item_names.append(ItemName.RARE_ITEM)

        for _ in range(self.multiworld.num_legendary_items[self.player]):
            item_names.append(ItemName.LEGENDARY_ITEM)

        itempool = [self.create_item(item_name) for item_name in item_names]
        logger.debug(f"Adding {len(itempool)} items")
        logger.debug(f"Number of locations: {len(location_table)}")
        self.multiworld.itempool += itempool

    def get_filler_item_name(self):
        return self.multiworld.random.choice(self._filler_items)
