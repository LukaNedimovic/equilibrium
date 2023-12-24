from utils.parser import parse_csv
from utils.data_wrapper import DataWrapper

def validate_login(username: str, password: str) -> bool:
    data = parse_csv("data\\user.csv")
    users = DataWrapper(data)
    found = users.find_match({"username": username, "password": password})
    
    return found