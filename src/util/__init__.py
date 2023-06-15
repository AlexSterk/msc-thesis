import typing

T = typing.TypeVar('T')


def find(pred: typing.Callable[[T], bool], iterable: typing.Iterable[T]) -> T:
    for element in iterable:
        if pred(element):
            return element
    return None
