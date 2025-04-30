#!/usr/bin/env python3

"""
sausage_links
=============

Implementation of the Sausage Links algorithm base Swinging Door in Python.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Generator, Iterator, Tuple, Union

    Source = Union[Generator, Iterator]
    Number = Union[int, float]
    Point = Tuple[Number, Number]
    Stretch = Tuple[Point, Point]
    Slopings = Tuple[float, float]
    Deviation = Union[Number, Tuple[Number, Number]]

__author__: str = "Aleksandr F. Mikhaylov (ChelAxe)"
__version__: str = "1.0.0"
__license__: str = "MIT"


def _sloping_calc(stretch: "Stretch", deviation: "Deviation") -> "Slopings":
    """
    Calculate slopings upper and lower.

    :param Stretch stretch: stretch;
    :param Deviation deviation: compression deflection.
    :rtype: Slopings
    :return: Slopings upper and lower.
    :raises ValueError: if division by 0 occurs during slope calculation.

    >>> _sloping_calc(((1, 6), (2, 6.5)), 1)
    (1.5, -0.5)

    >>> _sloping_calc(((1, 6), (2, 6.5)), (1, 1))
    (1.5, -0.5)

    >>> _sloping_calc(((1, 6), (1, 6.5)), 1)
    Traceback (most recent call last):
        ...
    ValueError: The division by 0 occurs during the calculation of the slope.
    """

    current: "Point"
    entrance: "Point"
    current, entrance = stretch

    dev_up: "Number"
    dev_down: "Number"

    if isinstance(deviation, tuple):
        dev_up, dev_down = deviation

    else:
        dev_up = dev_down = deviation

    dx: "Number" = current[0] - entrance[0]

    if not dx:
        raise ValueError(
            "The division by 0 occurs during the calculation of the slope."
        )

    upper: float = (current[1] - (entrance[1] + dev_up)) / dx
    lower: float = (current[1] - (entrance[1] - dev_down)) / dx

    return upper, lower


def sausage_links(  # pylint: disable=too-many-branches, too-many-statements
    source: "Source",
    deviation: "Deviation" = 0.1,
    max_len: "Number" = 0,
    auto_dev_factor: "Number" = 0,
    ema_alpha: "Number" = 0.3,
) -> "Generator[Point, None, None]":
    """
    Implementation of the Sausage Links algorithm base Swinging Door in Python.

    :param Source source: source data;
    :param Deviation deviation: compression deflection;
    :param Number max_len: maximum corridor length;
    :param Number auto_dev_factor: multiplier for EMA;
    :param Number ema_alpha: smoothing coefficient for EMA. [0; 1].
    :rtype: Generator[Point, None, None]
    :return: Compressed data.

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 8), (8, 9.5),
    ... ]), 1))
    [(1, 6), (7, 8), (8, 9.5)]

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 8), (8, 6),
    ... ]), 1))
    [(1, 6), (7, 8), (8, 6)]

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 8),
    ... ]), 1, 1))
    [(1, 6), (2, 6.5), (3, 5.5), (4, 6.5), (5, 8), (6, 7.5), (7, 8)]

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 9.5), (8, 8),
    ... ]), 1, auto_dev_factor=1))
    [(1, 6), (4, 6.5), (5, 8), (8, 8)]

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 3), (8, 8),
    ... ]), 1, auto_dev_factor=1))
    [(1, 6), (4, 6.5), (5, 8), (6, 7.5), (7, 3), (8, 8)]

    >>> list(sausage_links(iter([
    ...     (1, 6), (2, 6.5), (3, 5.5),
    ...     (4, 6.5), (5, 8), (6, 7.5),
    ...     (7, 8),
    ... ]), 0))
    [(1, 6), (2, 6.5), (3, 5.5), (4, 6.5), (5, 8), (6, 7.5), (7, 8)]

    >>> list(sausage_links(iter([]), 1))
    []

    >>> list(sausage_links(iter([(1, 6),]), 1))
    [(1, 6)]

    >>> list(sausage_links(iter([(1, 6),(1, 6.5),]), 1))
    Traceback (most recent call last):
        ...
    ValueError: The division by 0 occurs during the calculation of the slope.
    """

    if not deviation and not auto_dev_factor:
        yield from source
        return

    try:
        entrance: "Point" = next(source)

    except StopIteration:
        return

    yield entrance

    try:
        current: "Point" = next(source)

    except StopIteration:
        return

    current_deviation: "Deviation"

    if auto_dev_factor:
        dx: "Number" = current[0] - entrance[0]
        ema_slope: "float" = (
            (abs(current[1] - entrance[1]) / dx) if dx else 0.0
        )

        current_deviation = auto_dev_factor * ema_slope

    else:
        current_deviation = deviation

    sloping_upper: float
    sloping_lower: float
    sloping_upper, sloping_lower = _sloping_calc(
        (current, entrance), current_deviation
    )

    sloping_upper_max: float = sloping_upper
    sloping_lower_min: float = sloping_lower

    try:
        while True:
            past: "Point" = current
            current = next(source)

            if auto_dev_factor:
                dx = current[0] - past[0]
                ema_slope = (
                    ema_alpha
                    * ((abs(current[1] - past[1]) / dx) if dx else 0.0)
                    + (1 - ema_alpha) * ema_slope
                )

                current_deviation = auto_dev_factor * ema_slope

            if (
                max_len > 0  # pylint: disable=chained-comparison
                and abs(current[0] - entrance[0]) >= max_len
            ):
                yield past

                entrance = current
                yield entrance

                try:
                    current = next(source)

                except StopIteration:
                    return

                sloping_upper, sloping_lower = _sloping_calc(
                    (current, entrance), current_deviation
                )
                sloping_upper_max = sloping_upper
                sloping_lower_min = sloping_lower
                continue

            sloping_upper, sloping_lower = _sloping_calc(
                (current, entrance), current_deviation
            )

            if sloping_upper > sloping_upper_max:
                sloping_upper_max = sloping_upper

                if sloping_upper_max > sloping_lower_min:
                    yield past

                    entrance = current
                    yield entrance

                    try:
                        current = next(source)

                    except StopIteration:
                        return

                    if auto_dev_factor:
                        dx = current[0] - entrance[0]
                        ema_slope = (
                            ema_alpha
                            * (
                                (abs(current[1] - entrance[1]) / dx)
                                if dx
                                else 0.0
                            )
                            + (1 - ema_alpha) * ema_slope
                        )

                        current_deviation = auto_dev_factor * ema_slope

                    sloping_upper_max, sloping_lower_min = _sloping_calc(
                        (current, entrance), current_deviation
                    )

            elif sloping_lower < sloping_lower_min:
                sloping_lower_min = sloping_lower

                if sloping_upper_max > sloping_lower_min:
                    yield past

                    entrance = current
                    yield entrance

                    try:
                        current = next(source)

                    except StopIteration:
                        return

                    if auto_dev_factor:
                        dx = current[0] - entrance[0]
                        ema_slope = (
                            ema_alpha
                            * (
                                (abs(current[1] - entrance[1]) / dx)
                                if dx
                                else 0.0
                            )
                            + (1 - ema_alpha) * ema_slope
                        )

                        current_deviation = auto_dev_factor * ema_slope

                    sloping_upper_max, sloping_lower_min = _sloping_calc(
                        (current, entrance), current_deviation
                    )

    except StopIteration:
        yield past


if __name__ == "__main__":  # pragma: no cover
    import sys
    from doctest import testmod

    sys.exit(testmod().failed)
