def find_value(sorted_list, value, delta=0):
    """Check directly by bisection if sorted_list contains the required value
    (± delta if specified)."""

    lo = 0
    hi = len(sorted_list)

    while lo < hi:
        mid = (lo + hi) // 2
        if abs(sorted_list[mid] - value) <= delta:
            return True
        elif sorted_list[mid] < value:
            lo = mid + 1
        else:
            hi = mid

    return False


def find_sum_of_2_values(sorted_list, target_value, lo, hi, delta):
    """Check if sorted_list contains two elements between indices lo and hi
    whose sum is the target value (± delta if specified)"""

    while lo < hi:
        total_value = sorted_list[lo] + sorted_list[hi]
        if abs(total_value - target_value) <= delta:
            return True
        elif total_value < target_value:
            lo += 1
        else:
            hi -= 1

    return False


def find_sum_of_n_values(sorted_list, target_value, n, lo, hi, delta):
    """Check if sorted_list contains n elements between indices lo and hi
    whose sum is the target value (± delta if specified)"""

    if n == 2:
        return find_sum_of_2_values(sorted_list, target_value, lo, hi, delta)

    for i, i_value in enumerate(sorted_list[lo:], lo):
        new_target_value = target_value - i_value
        if find_sum_of_n_values(
            sorted_list, new_target_value, n - 1, i + 1, hi, delta
        ):
            return True

    return False


def plan_3_tracks(track_list, concert_premiere_length, delta=0):
    """Test if there are three elements in concert_premiere_length that sum up
    to concert_premiere_length.
    If delta is specified, the sum can fall within a margin of ±delta.
    """

    nb_tracks = len(track_list)
    if nb_tracks < 3:
        return False

    sorted_list = sorted(track_list)
    if sum(sorted_list[:3]) > concert_premiere_length + delta:
        return False
    if sum(sorted_list[-3:]) < concert_premiere_length - delta:
        return False

    for i, track_length in enumerate(sorted_list[:-2]):
        # Find two more tracks of greater or equal length, so that all three
        # lengths sum up to concert_premiere_length (±delta).
        target_length = concert_premiere_length - track_length
        if find_sum_of_2_values(
            sorted_list, target_length, i + 1, nb_tracks - 1, delta,
        ):
            return True

    return False


def plan_n_tracks(track_list, concert_premiere_length, n=3, delta=0):
    """Test if there are n elements (default: 3) in concert_premiere_length
    that sum up to concert_premiere_length.
    If delta is specified, the sum can fall within a margin of ±delta.
    """

    if n < 1:
        raise ValueError("n must be strictly positive.")

    nb_tracks = len(track_list)
    if nb_tracks < n:
        return False
    elif nb_tracks == n:
        return sum(track_list) == concert_premiere_length
    elif nb_tracks / 2 < n:
        # For large values of n, it is more efficient to find (nb_tracks - n)
        # tracks to EXCLUDE from the list.
        n = nb_tracks - n
        concert_premiere_length = sum(track_list) - concert_premiere_length

    sorted_list = sorted(track_list)
    if sum(sorted_list[:n]) > concert_premiere_length + delta:
        return False
    if sum(sorted_list[-n:]) < concert_premiere_length - delta:
        return False

    if n == 1:
        return find_value(sorted_list, concert_premiere_length, delta)
    elif n == 2:
        return find_sum_of_2_values(
            sorted_list, concert_premiere_length, 0, nb_tracks - 1, delta
        )
    else:
        return find_sum_of_n_values(
            sorted_list, concert_premiere_length, n, 0, nb_tracks - 1, delta
        )


def test():
    """Basic test suite using no external library."""
    track_list = [8, 6, 15, 2, 14, 40, 3]

    # Test the sanity checks
    assert not plan_3_tracks([10, 20], 30)
    assert not plan_3_tracks(track_list, 8)
    assert not plan_3_tracks(track_list, 300)

    # Test the default use case
    assert plan_3_tracks(track_list, 22)
    assert plan_3_tracks(track_list, 13)
    assert not plan_3_tracks(track_list, 43)
    assert not plan_3_tracks(track_list, 12)

    # Test the use case with delta
    assert plan_3_tracks(track_list, 66, delta=5)
    assert plan_3_tracks(track_list, 74, delta=5)
    assert not plan_3_tracks(track_list, 75, delta=5)

    # Test the sanity checks for plan_n_tracks
    assert plan_n_tracks(track_list, 88, n=7)
    assert not plan_n_tracks(track_list, 87, n=7)
    assert not plan_n_tracks(track_list, 88, n=8)
    assert not plan_3_tracks(track_list, 8)
    assert not plan_3_tracks(track_list, 300)

    # Test plan_n_tracks with n=1
    assert plan_n_tracks(track_list, 14, n=1)
    assert not plan_n_tracks(track_list, 10, n=1)
    assert plan_n_tracks(track_list, 35, n=1, delta=5)
    assert not plan_n_tracks(track_list, 22, n=1, delta=5)

    # Test plan_n_tracks with n=2
    assert plan_n_tracks(track_list, 14, n=2)
    assert not plan_n_tracks(track_list, 15, n=2)
    assert plan_n_tracks(track_list, 34, n=2, delta=5)
    assert not plan_n_tracks(track_list, 35, n=2, delta=5)

    # Test plan_n_tracks with n=3 (repeat the first tests with the new method)
    assert plan_n_tracks(track_list, 22, n=3)
    assert plan_n_tracks(track_list, 13, n=3)
    assert not plan_n_tracks(track_list, 43, n=3)
    assert not plan_n_tracks(track_list, 12, n=3)
    assert plan_n_tracks(track_list, 66, n=3, delta=5)
    assert plan_n_tracks(track_list, 74, n=3, delta=5)
    assert not plan_n_tracks(track_list, 75, n=3, delta=5)

    # Test plan_n_tracks with n=4
    assert plan_n_tracks(track_list, 71, n=4)
    assert not plan_n_tracks(track_list, 74, n=4)
    assert plan_n_tracks(track_list, 74, n=4, delta=5)
    assert plan_n_tracks(track_list, 14, n=4, delta=5)
    assert not plan_n_tracks(track_list, 13, n=4, delta=5)
    assert plan_n_tracks(track_list, 21, n=4, delta=2)
    assert not plan_n_tracks(track_list, 21, n=4, delta=1)

    # Test plan_n_tracks with n=5
    assert plan_n_tracks(track_list, 74, n=5)
    assert not plan_n_tracks(track_list, 28, n=5)
    assert plan_n_tracks(track_list, 28, n=5, delta=5)
    assert not plan_n_tracks(track_list, 27, n=5, delta=5)

    # Test plan_n_tracks with n=6
    assert plan_n_tracks(track_list, 48, n=6)
    assert not plan_n_tracks(track_list, 68, n=6)
    assert plan_n_tracks(track_list, 68, n=6, delta=5)
    assert not plan_n_tracks(track_list, 67, n=6, delta=5)
    assert plan_n_tracks(track_list, 90, n=6, delta=5)

    print("All tests executed successfully.")


if __name__ == "__main__":
    test()
