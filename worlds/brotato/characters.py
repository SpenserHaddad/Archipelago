import random
from typing import NamedTuple

from Options import OptionError

from .constants import ABYSSAL_TERRORS_CHARACTERS, BASE_GAME_CHARACTERS, CharacterGroup
from .options import StartingCharacters


class CharacterGroupInfo(NamedTuple):
    enabled: bool
    include_characters: set[str]
    group: CharacterGroup


class CharacterInfoOutput(NamedTuple):
    available_characters: list[str]
    starting_characters: list[str]


def get_available_and_starting_characters(
    include_base_game_characters: set[str],
    enable_abyssal_terrors_dlc: bool,
    include_abyssal_terrors_characters: set[str],
    starting_character_mode: StartingCharacters,
    num_starting_characters: int,
    num_available_characters: int,
    random: random.Random,
) -> CharacterInfoOutput:
    character_pack_info: dict[str, CharacterGroupInfo] = {
        BASE_GAME_CHARACTERS.name: CharacterGroupInfo(
            enabled=True,
            include_characters=include_base_game_characters,
            group=BASE_GAME_CHARACTERS,
        ),
        ABYSSAL_TERRORS_CHARACTERS.name: CharacterGroupInfo(
            enabled=enable_abyssal_terrors_dlc,
            include_characters=include_abyssal_terrors_characters,
            group=ABYSSAL_TERRORS_CHARACTERS,
        ),
    }

    included_characters: list[str] = []
    for pack_enabled, include_characters_from_pack, pack_characters in character_pack_info.values():
        if pack_enabled:
            included_characters = [c for c in pack_characters.characters if c in include_characters_from_pack]

    # Sort the characters so random selection is deterministic, then pick who to include to match the requested amount.
    included_characters.sort()
    available_characters = random.sample(included_characters, num_available_characters)

    starting_characters: list[str]
    match starting_character_mode.value:
        case StartingCharacters.option_default_all:
            enabled_groups: list[CharacterGroup] = [pack.group for pack in character_pack_info.values() if pack.enabled]
            starting_characters = [
                char for eg in enabled_groups for char in eg.default_characters if char in available_characters
            ]
        case StartingCharacters.option_random_all:
            starting_characters = random.sample(available_characters, num_starting_characters)
        case StartingCharacters.option_default_base_game:
            starting_characters = [
                char for char in BASE_GAME_CHARACTERS.default_characters if char in available_characters
            ]
        case StartingCharacters.option_random_base_game:
            starting_characters = random.sample(
                sorted(character_pack_info[BASE_GAME_CHARACTERS.name].include_characters), num_starting_characters
            )
        case StartingCharacters.option_default_abyssal_terrors:
            if not enable_abyssal_terrors_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Abyssal Terrors DLC is disabled."
                )
            starting_characters = [
                char for char in ABYSSAL_TERRORS_CHARACTERS.default_characters if char in available_characters
            ]
        case StartingCharacters.option_random_abyssal_terrors:
            if not enable_abyssal_terrors_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Abyssal Terrors DLC is disabled."
                )
            starting_characters = random.sample(
                sorted(character_pack_info[ABYSSAL_TERRORS_CHARACTERS.name].include_characters), num_starting_characters
            )
        case _:
            raise OptionError(f"Unknown value for starting character option: {starting_character_mode}")

    return CharacterInfoOutput(available_characters=available_characters, starting_characters=starting_characters)
