# https://adventofcode.com/2023/day/1
from typing import Final, Iterator

import aoc_itertools
import aoc_utils

NUMBERS_IN_WORDS_MAP: Final[dict[str, int]] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

POSSIBLE_WORD_SUBSTRINGS: Final[set[str]] = {
    word[:i] for word in NUMBERS_IN_WORDS_MAP.keys() for i in range(1, len(word) + 1)
}


def first_and_last_digit_word_or_numeral(
    string_to_check: str,
) -> tuple[int | None, int | None]:
    """
    Returns the first and last numbers found in a string, either as digits or words.

    return: A tuple containing the first and last numbers found, or None if not found.
    Could be made more efficient by searching starting from the end for `last_value`.
    """
    start_possible_digit_word_index = 0
    first_value, last_value = None, None
    for idx, char in enumerate(string_to_check):
        if char.isdigit():
            if first_value is None:
                first_value = int(char)
            last_value = int(char)

        possible_digit_word = string_to_check[start_possible_digit_word_index : idx + 1]

        if possible_digit_word in POSSIBLE_WORD_SUBSTRINGS:
            if value := NUMBERS_IN_WORDS_MAP.get(possible_digit_word):
                if first_value is None:
                    first_value = value
                last_value = value
        else:
            start_possible_digit_word_index = idx - 1

    return first_value, last_value


def combine_first_and_last_number(s: str, *, part_one: bool) -> int | None:
    # Find the first and last number in s, and concat them into one integer.
    # >> combine_first_and_last_number("t5st0")
    # >> 50
    # If part_one=False, we also check for word strings:
    # >> combine_first_and_last_number('abeight3andthe5nine', part_one=False)
    # >> 89
    # >> combine_first_and_last_number('abeight3andthe5nine', part_one=True)
    # >> 35

    if part_one:
        first = aoc_itertools.first_or_none(c for c in s if c.isdigit())
        last = aoc_itertools.first_or_none(c for c in reversed(s) if c.isdigit())
    else:
        first, last = map(str, first_and_last_digit_word_or_numeral(s))

    if first is not None and last is not None:
        return int(first + last)

    return None


def parse_calibration_document(filename: str, *, part_one: bool) -> Iterator[int]:
    # yield the calibration value for each line.
    doc_data = aoc_utils.load_input(filename)

    for line in doc_data.splitlines():
        if calibration_value := combine_first_and_last_number(line, part_one=part_one):
            yield calibration_value
        else:
            print(f"bad input: line '{line}' does not contain numbers.")


if __name__ == "__main__":
    assert sum(parse_calibration_document("example_part_one.txt", part_one=True)) == 142
    assert (
        sum(parse_calibration_document("example_part_two.txt", part_one=False)) == 281
    )
    print("Part one:", sum(parse_calibration_document("puzzle.txt", part_one=True)))
    print("Part two:", sum(parse_calibration_document("puzzle.txt", part_one=False)))
