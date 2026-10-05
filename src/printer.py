# JOB 4: print the edit script as bytes.
# - every output line is: prefix + exact line bytes + b"\n"
# - delete-first rule: in each change block, all '-' lines before any '+' line
# - highlight mode: after the i-th paired '+' line, print "? old | new"

import sys

import highlighter
import myers


def print_diff(ops, a, b, highlight):
    out = []                     # collect pieces, write once at the end (fast)
    i = j = 0                    # next line of A, next line of B
    p = 0                        # position in ops
    total = len(ops)
    while p < total:
        if ops[p] == myers.KEEP:
            out.append(b" " + a[i] + b"\n")
            i += 1
            j += 1
            p += 1
            continue
        # Collect one change block: everything up to the next KEEP
        dels, inss = [], []
        while p < total and ops[p] != myers.KEEP:
            if ops[p] == myers.DELETE:
                dels.append(a[i])
                i += 1
            else:
                inss.append(b[j])
                j += 1
            p += 1
        for line in dels:
            out.append(b"-" + line + b"\n")
        pairs = min(len(dels), len(inss))
        for t, line in enumerate(inss):
            out.append(b"+" + line + b"\n")
            if highlight and t < pairs:
                text = "? " + highlighter.ranges(dels[t], line) + "\n"
                out.append(text.encode("ascii"))
    sys.stdout.buffer.write(b"".join(out))
    sys.stdout.buffer.flush()