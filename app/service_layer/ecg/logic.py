import itertools
from typing import List


def calculate_zero_crossing(signal: List[int]):
    # remove zeros to avoid counting when it touches zero but not crossing.
    signal = filter(lambda x: x != 0, signal)

    # grouping by sign, then number of groups less one
    count = len(list(itertools.groupby(signal, lambda x: x > 0))) - 1

    return count
