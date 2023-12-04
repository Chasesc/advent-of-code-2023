# https://adventofcode.com/2023/day/2
import itertools
import re
from math import prod
from typing import Final, Iterable, Iterator, LiteralString, NotRequired, TypedDict, cast

import aoc_utils


class CubeColorCounts(TypedDict):
    red: NotRequired[int]
    green: NotRequired[int]
    blue: NotRequired[int]


PART_ONE_BAG_CONTENTS: Final[CubeColorCounts] = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

# Extract the count and color. i.e. " 3 blue"
GAME_SAMPLE_REGEX: LiteralString = r"(\d+) (\w+)"
ALLOWED_CUBE_COLORS: Final[set[str]] = set(color for color in PART_ONE_BAG_CONTENTS.keys())


class GameDetails(TypedDict):
    game_id: int
    # Each game is made up of multiple sample draws
    samples: list[CubeColorCounts]


def extract_game_details(game_details: str) -> GameDetails:
    # Extract game details from strings like
    # 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
    # Strings should always be in this format.
    # only minimal error handling is done.
    game_id, game_details = game_details.split(":")
    game_id_value = int("".join(itertools.dropwhile(lambda char: not char.isdigit(), game_id)))

    samples: list[CubeColorCounts] = []

    for sample in game_details.split(";"):
        colors_to_count: dict[str, int] = {}
        for individual_color_result in sample.split(","):
            result = re.search(GAME_SAMPLE_REGEX, individual_color_result)
            if result is None or len(result.groups()) != 2:
                raise ValueError(
                    f"something is off with color result='{individual_color_result}' from sample='{sample}'. game_id={game_id_value}"
                )

            count, color = result.groups()
            if color not in ALLOWED_CUBE_COLORS:
                raise ValueError(f"what are you doing. color={color} is not allowed.")

            colors_to_count[color] = int(count)

        samples.append(cast(CubeColorCounts, colors_to_count))

    return GameDetails(game_id=game_id_value, samples=samples)


def is_game_possible(game_details: GameDetails, bag_capacity: CubeColorCounts) -> bool:
    return all(
        sample.get("red", 0) <= bag_capacity["red"]
        and sample.get("blue", 0) <= bag_capacity["blue"]
        and sample.get("green", 0) <= bag_capacity["green"]
        for sample in game_details["samples"]
    )


def minimum_required_cube_color_counts(game_details: GameDetails) -> CubeColorCounts:
    min_red = max(sample.get("red", 0) for sample in game_details["samples"])
    min_blue = max(sample.get("blue", 0) for sample in game_details["samples"])
    min_green = max(sample.get("green", 0) for sample in game_details["samples"])
    return CubeColorCounts(red=min_red, blue=min_blue, green=min_green)


def parse_games_list_for_possible_game_ids(filename: str, *, part_one: bool) -> Iterator[int]:
    game_data = aoc_utils.load_input(filename)

    for line in game_data.splitlines():
        game_details = extract_game_details(line)

        if part_one and is_game_possible(game_details, PART_ONE_BAG_CONTENTS):
            yield game_details["game_id"]
        elif not part_one:
            values = minimum_required_cube_color_counts(game_details).values()
            yield prod(cast(Iterable[int], values))


if __name__ == "__main__":
    assert sum(parse_games_list_for_possible_game_ids("example.txt", part_one=True)) == 8
    assert sum(parse_games_list_for_possible_game_ids("example.txt", part_one=False)) == 2286
    print(
        "Part one:",
        sum(parse_games_list_for_possible_game_ids("puzzle.txt", part_one=True)),
    )
    print(
        "Part two:",
        sum(parse_games_list_for_possible_game_ids("puzzle.txt", part_one=False)),
    )
