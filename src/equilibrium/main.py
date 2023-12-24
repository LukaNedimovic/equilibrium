import time

from utils.keypress_detector import capture_keypress
from utils.data_wrapper import DataWrapper
from utils.parser import parse_csv
from utils.formatting import clear_screen

from prompt.main_prompt import MainPrompt

from user.users import Users

import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent

PATH_USERS_DATA = os.getenv("PATH_USERS_DATA")

def setup():
    user_data_parsed = parse_csv(project_root / PATH_USERS_DATA)
    user_data_wrapped = DataWrapper(user_data_parsed)

    global users
    users = Users()
    users.load_users(user_data_wrapped)


def main():
    current_prompt = MainPrompt("main")
    while True: 
        time.sleep(0.01)
        clear_screen()
        current_prompt.show()
        key = capture_keypress()
        if key is not None:
            response = current_prompt.parse_keypress(key)
            if type(response) == int and response == 1:
                current_prompt = current_prompt.next_prompt()
                
            elif type(response) == str:
                if response == "validate login":
                    username = current_prompt.entered_username
                    password = current_prompt.entered_password
                    
                    user_found = users.validate_login(username, password)
                    if user_found:
                        current_prompt = current_prompt.next_prompt()

                elif response == "validate sign up":
                    successfully_signed_up = users.sign_up_user(current_prompt.entered_values)
                    if successfully_signed_up:  
                        current_prompt = current_prompt.next_prompt()


if __name__ == "__main__":
    setup()
    main()