# JOB 1: Read a file as raw bytes and cut it into lines at every b"\n".
# Lines stay as bytes, so '\r' and non-UTF-8 bytes are kept exactly.


def read_lines(path):
    with open(path, "rb") as f:          # "rb" = read bytes, never text mode
        data = f.read()
    lines = data.split(b"\n")
    if lines[-1] == b"":                 # file ended with \n (or is empty): drop last piece
        lines.pop()
    return lines