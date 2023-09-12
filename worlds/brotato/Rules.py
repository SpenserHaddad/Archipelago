from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from .Constants import CHARACTERS

# from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import BrotatoWorld


def character_generic_completion_condition(num_required_wins: int, player: int, state: CollectionState) -> bool:
    return state.has("Run Complete", player, count=num_required_wins)


def character_specific_completion_condition(num_required_wins: int, player: int, state: CollectionState) -> bool:
    won_runs = 0
    for character in CHARACTERS:
        if state.has(f"Run Complete ({character})", player):
            won_runs += 1
    return won_runs >= num_required_wins


def set_rules(brotato_world: "BrotatoWorld", included_episodes):
    # player = brotato_world.player
    # world = brotato_world.multiworld
    pass
