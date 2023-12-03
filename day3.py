# https://adventofcode.com/2023/day/3
from typing import Final, Iterator

import aoc_utils

SYMBOLS: Final[set[str]] = set("#$%&*+-/=@")


def to_2d_list(input_string: str) -> list[list[str]]:
    # convert a string with newlines into a 2d (list of lists)
    # where each sub list contains a single character
    # 12..\n.45. => [["1", "2", ".", "."], [".", "4", "5", "."]]
    list_2d: list[list[str]] = []
    for line in input_string.splitlines():
        list_2d.append([c for c in line])

    if list_2d:
        first_list_len = len(list_2d[0])
        assert all(
            first_list_len == len(lst) for lst in list_2d[1:]
        ), "each line should be of the same length."
    else:
        raise ValueError("cannot create 2d list. no data.")

    return list_2d


def extract_numbers_and_bounds(
    engine_row: list[str],
) -> Iterator[tuple[int, tuple[int, int]]]:
    # [".", "4", "2", ".", "5", "."]
    # extracts [(42, (1, 2)), (5, (4, 4))]

    start_idx: int | None = None
    for idx, char in enumerate(engine_row):
        if char.isdigit():
            if start_idx is None:
                start_idx = idx
        elif start_idx is not None:
            digit = int("".join(engine_row[start_idx:idx]))
            yield (digit, (start_idx, idx - 1))
            start_idx = None

    if start_idx is not None:
        digit = int("".join(engine_row[start_idx:]))
        yield (digit, (start_idx, len(engine_row) - 1))


def find_numbers_adjacent_to_symbols(
    engine_schematic: list[list[str]], line_idx: int
) -> Iterator[int]:
    max_x, max_y = len(engine_schematic[0]) - 1, len(engine_schematic) - 1

    def is_in_bounds(x: int, y: int) -> bool:
        return x >= 0 and y >= 0 and x <= max_x and y <= max_y

    def get_adjacent_tiles(start_x_idx: int, end_x_idx: int) -> Iterator[str]:
        for y in (line_idx - 1, line_idx, line_idx + 1):
            # end is + 2, since the end is non-inclusive.
            for x in range(start_x_idx - 1, end_x_idx + 2):
                if is_in_bounds(x, y):
                    yield engine_schematic[y][x]

    engine_row = engine_schematic[line_idx]

    for number, (start_x_idx, end_x_idx) in extract_numbers_and_bounds(engine_row):
        if any(tile in SYMBOLS for tile in get_adjacent_tiles(start_x_idx, end_x_idx)):
            yield number


def parse_file_yielding_part_numbers(filename: str) -> Iterator[int]:
    engine_schematic_input = aoc_utils.load_input(filename)
    engine_schematic = to_2d_list(engine_schematic_input)

    for line_idx in range(len(engine_schematic)):
        yield from find_numbers_adjacent_to_symbols(engine_schematic, line_idx=line_idx)


if __name__ == "__main__":
    assert sum(parse_file_yielding_part_numbers("example.txt")) == 4361
    print("Part one:", sum(parse_file_yielding_part_numbers("puzzle.txt")))
