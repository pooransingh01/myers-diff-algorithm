# PART B: for one changed line pair, find which characters changed.
# Runs Myers again on the characters (Unicode code points) of the two lines
# and returns the text after "? ", like "12-13 | 11-12".

import myers


def ranges(old_line, new_line):
    # A Python str is a sequence of code points, so an emoji counts as one character
    x = old_line.decode("utf-8")
    y = new_line.decode("utf-8")
    ops = myers.diff(x, y)

    old_r, new_r = [], []
    i = j = 0                    # position in old line, position in new line
    old_start = new_start = -1   # start of the open range, -1 = no open range

    for op in ops:
        if op == myers.KEEP:
            # A kept character ends any open range
            if old_start >= 0:
                old_r.append(f"{old_start}-{i}")
                old_start = -1
            if new_start >= 0:
                new_r.append(f"{new_start}-{j}")
                new_start = -1
            i += 1
            j += 1
        elif op == myers.DELETE:
            if old_start < 0:
                old_start = i
            i += 1
        else:
            if new_start < 0:
                new_start = j
            j += 1
    if old_start >= 0:
        old_r.append(f"{old_start}-{i}")
    if new_start >= 0:
        new_r.append(f"{new_start}-{j}")

    o = ",".join(old_r) if old_r else "."
    n = ",".join(new_r) if new_r else "."
    return f"{o} | {n}"