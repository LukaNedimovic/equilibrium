class DataWrapper:
    def __init__(self, data):
        self.column_names = data[0] # column names
        self.data         = data[1:]

    def __getitem__(self, arg) -> dict:
        return self.data[arg]

    def find_match(self, pattern: dict) -> bool:
        for row in self.data:
            if all(row[key] == value for key, value in pattern.items()):
                return True
        return False