import re

pattern = re.compile(r'("(?:[^"]|"")*"|[^,]+)(?:,|$)')


def parse_txt_line(line: str):
    """
    Parses a singular ".txt" line, as intended.

    Parameters
    ----------
    line : str
        Line to be parsed.

    Returns
    -------
    dict
        Returns dictionary, where key is the first value in the line,
        (so, before ":" symbol), while the value is everything else.
    """
    split_line = line.split(":")
    key = split_line[0]
    value = split_line[1].strip("\n")

    return (key, value)


def parse_csv(path: str) -> list:
    """
    Parse an entire ".csv" file.

    Parameters
    ----------
    path : str
        DESCRIPTION.

    Returns
    -------
    list
        Returns a list containing the column names of the ".csv" file in the 
        first entry.
        Every other entry is dictionary, where the "key" is column name,
        and "value" is the value present in the respectable position.
    """
    
    csv_file = open(path, encoding="utf8") # Open file 
    lines = csv_file.readlines()    # Read file

    parsed_csv = []

    column_names = parse_csv_line(lines[0]) # Get the column names
    parsed_csv.append(column_names) # Push them as the first entry

    # Parse lines after the header
    for line in lines[1:]:
        if len(line) == 0 or line == "\n":
            continue
        
        parsed_line = parse_csv_line(line)
        parsed_line_dict = {}

        pos = 0
        for column_name in column_names:
            parsed_line_dict[column_name] = parsed_line[pos]
            pos += 1
        
        parsed_csv.append(parsed_line_dict)

    csv_file.close()
    return parsed_csv

def parse_csv_line(line: str) -> list:
    """
    Parses a singular ".csv" line.

    Parameters
    ----------
    line : str
        Line to be parsed.

    Returns
    -------
    list
        Returns a list of tokens, separated by "," in the passed line.
    """
    # parsed_line = line.strip("\n").split(",")
    line = line.strip("\n")
    
    res = [match.group(1).replace('""', '"') if match.group(1) else '' for match in pattern.finditer(line)]
    return res
    
    # return parsed_line


def write_line_csv(path: str, line: str) -> list:
    """
    Writes a line to the csv file.

    Parameters
    ----------
    path : str
        Path to the desired csv file.
    line : str
        Line to be appended to the ".csv" file.

    Returns
    -------
    list
        DESCRIPTION.

    """
    csv_file = open(path, "a", encoding="utf8")
    
    csv_file.write(line) # Append the line to the end of the file
    
    csv_file.close()
