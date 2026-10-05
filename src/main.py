# MANAGER: checks the command, then calls the other files in order.
#   python main.py lines A B       -> Part A
#   python main.py highlight A B   -> Part B

import sys

import line_numberer
import line_reader
import myers
import printer


def main():
    args = sys.argv[1:]
    if len(args) != 3 or args[0] not in ("lines", "highlight"):
        print("usage: main.py lines|highlight A_PATH B_PATH", file=sys.stderr)
        sys.exit(2)
    command, a_path, b_path = args

    # Job 1: read both files. If one can't be read: nothing on stdout, message on stderr, exit 2.
    try:
        a = line_reader.read_lines(a_path)
        b = line_reader.read_lines(b_path)
    except OSError as e:
        print(f"error: cannot read file: {e}", file=sys.stderr)
        sys.exit(2)

    # Job 2: give each line a number (one book shared by both files)
    book = {}
    a_ids = line_numberer.to_ids(a, book)
    b_ids = line_numberer.to_ids(b, book)

    # Job 3: Myers finds the minimal edit script
    ops = myers.diff(a_ids, b_ids)

    # Job 4: print it (with character ranges when the command is "highlight")
    printer.print_diff(ops, a, b, command == "highlight")


if __name__ == "__main__":
    main()