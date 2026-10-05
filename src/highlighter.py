import myers


def ranges(old_line, new_line):
    old_text = old_line.decode("utf-8")
    new_text = new_line.decode("utf-8")
    ops = myers.diff(old_text, new_text)

    old_ranges, new_ranges = [], []
    old_index = new_index = 0
    old_range_start = new_range_start = None

    for op in ops:
        if op == myers.KEEP:
            if old_range_start is not None:
                old_ranges.append(f"{old_range_start}-{old_index}")
                old_range_start = None
            if new_range_start is not None:
                new_ranges.append(f"{new_range_start}-{new_index}")
                new_range_start = None
            old_index += 1
            new_index += 1
        elif op == myers.DELETE:
            if old_range_start is None:
                old_range_start = old_index
            old_index += 1
        else:
            if new_range_start is None:
                new_range_start = new_index
            new_index += 1

    if old_range_start is not None:
        old_ranges.append(f"{old_range_start}-{old_index}")
    if new_range_start is not None:
        new_ranges.append(f"{new_range_start}-{new_index}")

    old_summary = ",".join(old_ranges) if old_ranges else "."
    new_summary = ",".join(new_ranges) if new_ranges else "."
    return f"{old_summary} | {new_summary}"