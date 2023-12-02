from typing import Iterator, TypeVar

T = TypeVar("T")


def first_or_none(it: Iterator[T]) -> T | None:
    try:
        return next(it)
    except StopIteration:
        return None
