from __future__ import annotations

from BaseClasses import MultiWorld, Region

from .Locations import location_table


def create_regions(world: MultiWorld, player: int):
    menu_region = Region("Menu", player, world)
    wave_region = Region("In-Game", player, world)
    shop_region = Region("Shop", player, world)
    menu_region.connect(wave_region, "Start Run")
    wave_region.connect(shop_region, "Wave Complete")
    wave_region.connect(menu_region, "Run Complete or Lost")
    shop_region.connect(wave_region, "Start New Wave")

    wave_region.add_locations({loc.name: loc.id for loc in location_table})
    world.regions += [menu_region, wave_region, shop_region]
