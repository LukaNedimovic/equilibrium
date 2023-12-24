def parse_txt_line(line: str) -> dict:
    split_line = line.split(":")
    key = split_line[0]
    value = split_line[1].strip("\n")

    return (key, value)

def parse_csv(path: str) -> list:
    csv_file = open(path) # Open file 
    lines = csv_file.readlines()    # Read file

    parsed_csv = []

    column_names = parse_csv_line(lines[0])
    parsed_csv.append(column_names)

    for line in lines[1:]:
        parsed_line = parse_csv_line(line)
        parsed_line_dict = {}

        # napravi iterable
        pos = 0
        for column_name in column_names:
            parsed_line_dict[column_name] = parsed_line[pos]
            pos += 1

        parsed_csv.append(parsed_line_dict)

    csv_file.close()
    return parsed_csv

def parse_csv_line(line: str) -> list:
    parsed_line = line.strip("\n").split(",")
    return parsed_line

def write_line_csv(path: str, line: str) -> list:
    csv_file = open(path, "a")
    
    csv_file.write(line)
    
    csv_file.close()
