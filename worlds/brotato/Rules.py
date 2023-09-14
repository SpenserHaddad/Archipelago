from functools import partial
from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState

from .Constants import CHARACTERS
from .Items import ItemName

# from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import BrotatoWorld


def _get_completion_condition(world: BrotatoWorld) -> Callable[[CollectionState], bool]:
    num_required_wins = world.runs_required[world.player]
    if world.brotato_win_option[world.player] == "any":
        return partial(_completion_condition_any_character, num_required_wins, world.player)
    else:
        return partial(_completion_condition_specific_character, num_required_wins, world.player)


def _completion_condition_any_character(num_required_wins: int, player: int, state: CollectionState) -> bool:
    return state.has(ItemName.RUN_COMPLETE.value, player, count=num_required_wins)


def _completion_condition_specific_character(num_required_wins: int, player: int, state: CollectionState) -> bool:
    won_runs = 0
    for character in CHARACTERS:
        if state.has(f"Run Complete ({character})", player):
            won_runs += 1
    return won_runs >= num_required_wins


def set_rules(world: BrotatoWorld):
    world.multiworld.completion_condition[world.player] = _get_completion_condition(world)
    # player = brotato_world.player
    # world = brotato_world.multiworld
    pass
