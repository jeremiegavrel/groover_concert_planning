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
        lo = i + 1
        hi = nb_tracks - 1

        while lo < hi:
            total_length = track_length + sorted_list[lo] + sorted_list[hi]
            if abs(total_length - concert_premiere_length) <= delta:
                return True
            elif total_length < concert_premiere_length:
                lo += 1
            else:
                hi -= 1

    return False


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

    print("All tests executed successfully.")


if __name__ == "__main__":
    test()
