def plan_3_tracks(track_list, concert_premiere_length):
    """Test if there are three elements in concert_premiere_length that sum up
    to concert_premiere_length.
    """

    nb_tracks = len(track_list)
    if nb_tracks < 3:
        return False

    sorted_list = sorted(track_list)
    if sum(sorted_list[:3]) > concert_premiere_length:
        return False
    if sum(sorted_list[-3:]) < concert_premiere_length:
        return False

    for i, track_length in enumerate(sorted_list[:-2]):
        lo = i + 1
        hi = nb_tracks - 1

        while lo < hi:
            total_length = track_length + sorted_list[lo] + sorted_list[hi]
            if total_length < concert_premiere_length:
                lo += 1
            elif total_length > concert_premiere_length:
                hi -= 1
            else:
                return True

    return False


def test():
    """Basic test suite using no external library."""
    track_list = [8, 6, 15, 2, 14, 40, 3]
    assert plan_3_tracks(track_list, 22)
    assert plan_3_tracks(track_list, 13)
    assert not plan_3_tracks(track_list, 43)
    assert not plan_3_tracks(track_list, 12)
    print("All tests executed successfully.")


if __name__ == "__main__":
    test()
