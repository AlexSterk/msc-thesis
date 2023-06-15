with open("data/repos.txt") as f:
    lines = f.readlines()


def parse_line(line: str):
    return f"'{line.strip().lower()}'"


output = ",\n".join(map(parse_line, lines))
print(output)
