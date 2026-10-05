KEEP = 0
DELETE = 1
INSERT = 2


def diff(old_items, new_items):
    old_length, new_length = len(old_items), len(new_items)

    prefix_length = 0
    while (
        prefix_length < old_length
        and prefix_length < new_length
        and old_items[prefix_length] == new_items[prefix_length]
    ):
        prefix_length += 1

    suffix_length = 0
    while (
        suffix_length < old_length - prefix_length
        and suffix_length < new_length - prefix_length
        and old_items[old_length - 1 - suffix_length] == new_items[new_length - 1 - suffix_length]
    ):
        suffix_length += 1

    middle_ops = _shortest_edit_script(
        old_items[prefix_length:old_length - suffix_length],
        new_items[prefix_length:new_length - suffix_length],
    )
    return [KEEP] * prefix_length + middle_ops + [KEEP] * suffix_length


def _shortest_edit_script(old_items, new_items):
    trace, edit_count = _forward_search(old_items, new_items)
    return _backtrack(trace, edit_count, len(old_items), len(new_items))


def _came_from_above(furthest_old_index, diagonal, edit_count):
    return diagonal == -edit_count or (
        diagonal != edit_count
        and furthest_old_index[diagonal - 1] < furthest_old_index[diagonal + 1]
    )


def _snapshot(furthest_old_index, edit_count):
    if edit_count == 0:
        return furthest_old_index[:1]
    buffer_size = len(furthest_old_index)
    return furthest_old_index[:edit_count + 1] + furthest_old_index[buffer_size - edit_count:]


def _forward_search(old_items, new_items):
    old_length, new_length = len(old_items), len(new_items)
    max_edits = old_length + new_length
    furthest_old_index = [0] * (2 * max_edits + 3)
    trace = []
    final_edit_count = 0

    for edit_count in range(max_edits + 1):
        reached_end = False
        for diagonal in range(-edit_count, edit_count + 1, 2):
            if _came_from_above(furthest_old_index, diagonal, edit_count):
                old_index = furthest_old_index[diagonal + 1]
            else:
                old_index = furthest_old_index[diagonal - 1] + 1
            new_index = old_index - diagonal

            while (
                old_index < old_length
                and new_index < new_length
                and old_items[old_index] == new_items[new_index]
            ):
                old_index += 1
                new_index += 1

            furthest_old_index[diagonal] = old_index
            if old_index >= old_length and new_index >= new_length:
                final_edit_count = edit_count
                reached_end = True
                break

        trace.append(_snapshot(furthest_old_index, edit_count))
        if reached_end:
            break

    return trace, final_edit_count


def _backtrack(trace, edit_count, old_length, new_length):
    reversed_ops = []
    old_index, new_index = old_length, new_length

    for current_edits in range(edit_count, 0, -1):
        previous_round = trace[current_edits - 1]
        diagonal = old_index - new_index

        if _came_from_above(previous_round, diagonal, current_edits):
            previous_diagonal = diagonal + 1
        else:
            previous_diagonal = diagonal - 1
        previous_old_index = previous_round[previous_diagonal]
        previous_new_index = previous_old_index - previous_diagonal

        while old_index > previous_old_index and new_index > previous_new_index:
            reversed_ops.append(KEEP)
            old_index -= 1
            new_index -= 1

        reversed_ops.append(INSERT if previous_diagonal == diagonal + 1 else DELETE)
        old_index, new_index = previous_old_index, previous_new_index

    while old_index > 0 and new_index > 0:
        reversed_ops.append(KEEP)
        old_index -= 1
        new_index -= 1

    reversed_ops.reverse()
    return reversed_ops