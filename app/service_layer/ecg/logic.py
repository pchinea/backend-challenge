import itertools


def calculate_zero_crossing(signal: list[int]):
    # remove zeros to avoid counting when it touches zero but not crossing.
    signal = filter(lambda x: x != 0, signal)

    # grouping by sign, number of groups less one
    count = len(list(itertools.groupby(signal, lambda x: x > 0))) - 1

    return count
