import typing

from Options import AssembleOptions, Range


class NumberVictories(Range):
    """
    The number of run wins required for Victory.
    """

    range_start = 0
    range_end = 44

    display_name = "Number of Victories"
    default = 10


options: typing.Dict[str, AssembleOptions] = {
    "num_victories": NumberVictories,
}
