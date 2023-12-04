# https://adventofcode.com/2023/day/4

import itertools
import re
from dataclasses import dataclass
from typing import Iterator

import aoc_utils


@dataclass(slots=True, frozen=True)
class Scorecard:
    card_id: int
    winning_numbers: set[int]
    my_numbers: set[int]

    def match_count(self) -> int:
        return len(self.winning_numbers & self.my_numbers)

    def score(self) -> int:
        return int(2 ** (self.match_count() - 1))


def extract_numbers(numbers_in_string: str) -> set[int]:
    return {int(n) for n in re.findall(r"\d+", numbers_in_string)}


def parse_scorecard_row(scorecard: str) -> Scorecard:
    card_id, card_numbers = scorecard.split(":")
    card_id_value = int("".join(itertools.dropwhile(lambda char: not char.isdigit(), card_id)))

    winning_numbers, my_numbers = card_numbers.split("|")
    return Scorecard(
        card_id=card_id_value, winning_numbers=extract_numbers(winning_numbers), my_numbers=extract_numbers(my_numbers)
    )


def parse_scorecards_yielding_points(filename: str) -> Iterator[int]:
    scorecard_data = aoc_utils.load_input(filename)

    for scorecard in scorecard_data.splitlines():
        yield parse_scorecard_row(scorecard).score()


if __name__ == "__main__":
    assert sum(parse_scorecards_yielding_points("example.txt")) == 13
    print("Part one:", sum(parse_scorecards_yielding_points("puzzle.txt")))
