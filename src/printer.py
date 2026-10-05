import sys

import highlighter
import myers


def print_diff(ops, old_lines, new_lines, highlight):
    output = []
    old_index = new_index = 0
    op_index = 0
    total_ops = len(ops)

    while op_index < total_ops:
        if ops[op_index] == myers.KEEP:
            output.append(b" " + old_lines[old_index] + b"\n")
            old_index += 1
            new_index += 1
            op_index += 1
            continue

        deleted_lines, inserted_lines = [], []
        while op_index < total_ops and ops[op_index] != myers.KEEP:
            if ops[op_index] == myers.DELETE:
                deleted_lines.append(old_lines[old_index])
                old_index += 1
            else:
                inserted_lines.append(new_lines[new_index])
                new_index += 1
            op_index += 1

        _append_change_block(output, deleted_lines, inserted_lines, highlight)

    sys.stdout.buffer.write(b"".join(output))
    sys.stdout.buffer.flush()


def _append_change_block(output, deleted_lines, inserted_lines, highlight):
    for line in deleted_lines:
        output.append(b"-" + line + b"\n")

    paired_count = min(len(deleted_lines), len(inserted_lines))
    for position, line in enumerate(inserted_lines):
        output.append(b"+" + line + b"\n")
        if highlight and position < paired_count:
            change_ranges = highlighter.ranges(deleted_lines[position], line)
            output.append(("? " + change_ranges + "\n").encode("ascii"))