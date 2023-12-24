from user.user import User
from utils.data_wrapper import DataWrapper
from utils.parser import write_line_csv

class Users:
    def __init__(self):
        self.users = []

    def __getitem__(self, arg) -> User:
        return self.users[arg]
    
    def load_users(self, wrapped_data: DataWrapper):
        for row in wrapped_data.data:
            new_user = User(row)
            self.users.append(new_user)
        
        for user in self.users:
            print(user)    

    def validate_login(self, username: str, password: str) -> bool:
        return any((user.username == username and user.password == password) for user in self.users)
    
    def username_exists(self, username: str) -> bool:
        return any((user.username == username) for user in self.users)

    def sign_up_user(self, user_data: dict):
        print(user_data)
        if self.username_exists(user_data["username"]):
            return False
        else:
            user = User(user_data)
            user.id = len(self.users)
            
            write_line_csv("data\\user.csv", user.to_csv_row())            
            self.users.append(user)
            return True
