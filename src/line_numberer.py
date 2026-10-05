def to_ids(lines, line_to_id):
    ids = []
    for line in lines:
        line_id = line_to_id.get(line)
        if line_id is None:
            line_id = len(line_to_id)
            line_to_id[line] = line_id
        ids.append(line_id)
    return ids