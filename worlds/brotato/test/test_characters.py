import random

from ..characters import get_available_and_starting_characters
from ..constants import ABYSSAL_TERRORS_CHARACTERS, BASE_GAME_CHARACTERS
from ..options import StartingCharacters
from . import BrotatoTestBase


class TestBrotatoCharacterOptions(BrotatoTestBase):
    """Tests to ensure that we correctly determine the included and starting characters from options.

    This differs from `test_include_characters` and `test_starting_characters` in that it focuses on checking that the
    output from `get_available_and_starting_characters` is correct, rather than checking that the generated items,
    locations, etc. are correct.
    """

    def test_base_game_default_starting_characters_correct(self):
        available_characters, starting_characters = get_available_and_starting_characters(
            set(BASE_GAME_CHARACTERS.characters),
            False,
            set(ABYSSAL_TERRORS_CHARACTERS.characters),
            StartingCharacters(StartingCharacters.option_default_base_game),
            BASE_GAME_CHARACTERS.num_default_characters,
            20,
            random.Random(0x7A70),
        )

        assert set(starting_characters) == set(BASE_GAME_CHARACTERS.default_characters)
