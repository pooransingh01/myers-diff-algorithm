import sys

import line_numberer
import line_reader
import myers
import printer

USAGE = "usage: main.py lines|highlight A_PATH B_PATH"
COMMANDS = ("lines", "highlight")


def main():
    arguments = sys.argv[1:]
    if len(arguments) != 3 or arguments[0] not in COMMANDS:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    command, old_path, new_path = arguments

    try:
        old_lines = line_reader.read_lines(old_path)
        new_lines = line_reader.read_lines(new_path)
    except OSError as error:
        print(f"error: cannot read file: {error}", file=sys.stderr)
        sys.exit(2)

    line_to_id = {}
    old_ids = line_numberer.to_ids(old_lines, line_to_id)
    new_ids = line_numberer.to_ids(new_lines, line_to_id)

    ops = myers.diff(old_ids, new_ids)

    printer.print_diff(ops, old_lines, new_lines, command == "highlight")


if __name__ == "__main__":
    main()