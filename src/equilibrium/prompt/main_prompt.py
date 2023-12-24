from .prompt import Prompt
from .login_prompt import LoginPrompt
from .sign_up_prompt import SignUpPrompt
from utils.formatting import bold

import sys

class MainPrompt(Prompt):
    def __init__(self, prompt_name: str):
        super().__init__(prompt_name)

        self.radio_selection = 1
        self.radio_selection_size = len(self.data["OPTIONS"])

        self.radio_selection_function = {1: self.login, 2: self.sign_up, 3: self.exit}
        self.next_prompt = None


    def show(self):
        ui = open(self.ui_path, encoding="utf8")
        lines = ui.readlines()
        for line in lines:
            if f"({self.radio_selection})" in line:
                line = bold(line, start=1, end=len(line)-2)    
            print(line, end="")

    def parse_keypress(self, key) -> int:
        response = -1 

        if key == "up":
            self.radio_selection -= 1 
            if self.radio_selection == 0:
                self.radio_selection = self.radio_selection_size       

        elif key == "down":
            self.radio_selection += 1
            if self.radio_selection == self.radio_selection_size + 1:
                self.radio_selection = 1

        elif key == "enter":
            self.next_prompt = self.radio_selection_function[self.radio_selection]
            response = 1
            
        return response

    # Loads Login prompt
    def login(self):
        login_prompt = LoginPrompt("login")
        return login_prompt
    
    # Loads Sign Up prompt
    def sign_up(self):
        sign_up_prompt = SignUpPrompt("sign_up")
        return sign_up_prompt
    
    def exit(self):
        sys.exit()