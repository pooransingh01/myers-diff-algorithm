def read_lines(path):
    with open(path, "rb") as file:
        content = file.read()

    lines = content.split(b"\n")
    if lines[-1] == b"":
        lines.pop()
    return lines