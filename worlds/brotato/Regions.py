from __future__ import annotations
from functools import partial

from BaseClasses import CollectionState, MultiWorld, Region

from .Constants import CHARACTERS, NUM_WAVES
from .Locations import character_specific_locations, location_name_to_id


def _has_character_rule(character: str, player: int, state: CollectionState) -> bool:
    return state.has(character, player, count=1)


def _always_accessible_rule(state: CollectionState) -> bool:
    return True


def create_regions(world: MultiWorld, player: int):
    menu_region = Region("Menu", player, world)
    crate_drop_region = Region("Loot Crates", player, world)

    crate_drop_locs_name_to_id = {}
    for i in range(world.num_common_crate_drops[player]):  # type: ignore
        loc_name = f"Crate Drop {i}"
        crate_drop_locs_name_to_id[loc_name] = location_name_to_id[loc_name]

    for i in range(world.num_legendary_crate_drops[player]):  # type: ignore
        loc_name = f"Legendary Crate Drop {i}"
        crate_drop_locs_name_to_id[loc_name] = location_name_to_id[loc_name]

    crate_drop_region.add_locations(crate_drop_locs_name_to_id)  # type: ignore
    menu_region.connect(crate_drop_region, "Drop Loot Crates")

    world.regions += [menu_region, crate_drop_region]

    character_regions = []
    waves_with_drops = list(range(0, NUM_WAVES, getattr(world, "waves_per_drop")[player]))[1:]
    for character in CHARACTERS:
        char_in_game_region = Region(f"In-Game ({character})", player, world)
        char_in_game_locations = character_specific_locations[character]
        char_in_game_region.add_locations(char_in_game_locations)
        char_region_access_rule = partial(_has_character_rule, character, player)
        char_wave_drop_location_names = [f"Wave {w} Complete ({character})" for w in waves_with_drops]
        char_in_game_region.add_locations({loc: location_name_to_id[loc] for loc in char_wave_drop_location_names})
        menu_region.connect(char_in_game_region, f"Start Game ({character})", rule=char_region_access_rule)

        # Crates can be gotten with any character
        char_in_game_region.connect(crate_drop_region, f"Drop crates for {character}")
        crate_drop_region.connect(char_in_game_region, f"Exit drop crates for {character}")
        character_regions.append(char_in_game_region)

    world.regions += character_regions
