# JOB 3: Myers' O(ND) algorithm. Works on any sequence whose items can be
# compared with == : line ids for Part A, characters of a str for Part B.
# Returns the edit script: a list of KEEP / DELETE / INSERT with the
# fewest possible DELETE + INSERT.

KEEP = 0
DELETE = 1
INSERT = 2


def diff(a, b):
    n, m = len(a), len(b)

    # Shortcut: equal items at the start and end are always KEEP.
    pre = 0
    while pre < n and pre < m and a[pre] == b[pre]:
        pre += 1
    suf = 0
    while suf < n - pre and suf < m - pre and a[n - 1 - suf] == b[m - 1 - suf]:
        suf += 1

    middle = _search(a[pre:n - suf], b[pre:m - suf])
    return [KEEP] * pre + middle + [KEEP] * suf


def _search(a, b):
    n, m = len(a), len(b)
    max_d = n + m
    # v[k] = furthest x reached on diagonal k.
    # Python trick: a negative index counts from the end of the list, so v[-3]
    # works directly for diagonal k = -3. The list is long enough that the
    # positive and negative parts never overlap.
    v = [0] * (2 * max_d + 3)
    size = len(v)
    trace = []                            # copy of v[-d..d] after each round d
    found_d = 0

    # ---- Forward search: round d = paths that use exactly d edits ----
    done = False
    for d in range(max_d + 1):
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                x = v[k + 1]              # come from diagonal k+1: move down = INSERT
            else:
                x = v[k - 1] + 1          # come from diagonal k-1: move right = DELETE
            y = x - k
            # Follow the snake: free diagonal moves while the items are equal
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x
            if x >= n and y >= m:         # reached the end (n, m) with d edits
                found_d = d
                done = True
                break
        # Save only diagonals -d..d (2d+1 values), not the whole list.
        # Stored as [v[0..d], v[-d..-1]] so prev[k] works for negative k too.
        trace.append(v[:d + 1] + v[size - d:] if d > 0 else v[:1])
        if done:
            break

    # ---- Backtrack: walk from (n, m) back to (0, 0) ----
    ops = []                              # built backwards, reversed once at the end
    x, y = n, m
    for d in range(found_d, 0, -1):
        prev = trace[d - 1]               # v after round d-1 (diagonals -(d-1)..(d-1))
        k = x - y
        if k == -d or (k != d and prev[k - 1] < prev[k + 1]):
            prev_k = k + 1                # we came down
        else:
            prev_k = k - 1                # we came right
        prev_x = prev[prev_k]
        prev_y = prev_x - prev_k

        while x > prev_x and y > prev_y:  # undo the snake: these were KEEPs
            ops.append(KEEP)
            x -= 1
            y -= 1
        ops.append(INSERT if prev_k == k + 1 else DELETE)  # the one edit of this round
        x, y = prev_x, prev_y
    while x > 0 and y > 0:                # the snake of round 0
        ops.append(KEEP)
        x -= 1
        y -= 1

    ops.reverse()
    return ops