# JOB 2: Give every distinct line a number (like a roll number).
# The same line always gets the same number, in both files,
# so Myers compares small ints instead of long byte strings.


def to_ids(lines, book):
    ids = []
    for line in lines:
        line_id = book.get(line)         # seen this line before?
        if line_id is None:              # no: give it the next new number
            line_id = len(book)
            book[line] = line_id
        ids.append(line_id)
    return ids