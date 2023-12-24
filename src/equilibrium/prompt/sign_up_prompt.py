from .prompt import Prompt
from .login_prompt import LoginPrompt
from .placeholder_prompt import PlaceholderPrompt

from utils.formatting import bold
from utils.data_validator import validate_login

import sys

import os
from dotenv import load_dotenv

load_dotenv()

PERMITTED_CHARS = os.getenv("PERMITTED_CHARS") 

class SignUpPrompt(Prompt):
    def __init__(self, prompt_name: str):
        super().__init__(prompt_name)

        self.radio_selection = 0
        self.radio_selection_size = len(self.data["OPTIONS"])
        self.input_placeholder = "!"
        self.label             = "Username"
        self.placeholder = {"Username":      "!", 
                            "Password":      "$",
                            "Name":          "+",
                            "Surname":       "-",
                            "Date of birth": "^",
                            "Residence":     ",",
                            "Profession":    ";"}
        self.buffer = {"Username":      ["_"] * 32, 
                       "Password":      ["_"] * 32,
                       "Name":          ["_"] * 32,
                       "Surname":       ["_"] * 32,
                       "Date of birth": ["_"] * 10,
                       "Residence":     ["_"] * 32,
                       "Profession":    ["_"] * 32}
        self.buffer_position = {"Username":      0, 
                                "Password":      0,
                                "Name":          0,
                                "Surname":       0,
                                "Date of birth": 0,
                                "Residence":     0,
                                "Profession":    0}
        self.entered_values = {"Username":      "",
                               "Password":      "",
                               "Name":          "",
                               "Surname":       "",
                               "Date of birth": "",
                               "Residence":     "",
                               "Profession":    ""}
        
        self.next_prompt = LoginPrompt("login")


    def show(self):
        ui = open(self.ui_path, encoding="utf8")
        lines = ui.readlines()
        for line in lines:

            if any(label in line for label in self.data["OPTIONS"]):
                found_label = [label for label in self.data["OPTIONS"]if label in line][0]
                input_placeholder = self.placeholder[found_label]

                input_start = line.find(input_placeholder)
                input_end   = line.rfind(input_placeholder)

                # print(input_start)

                line_list   = [char for char in line]
                for pos in range(0, len(self.buffer[found_label])):
                    line_list[input_start + pos] = self.buffer[found_label][pos]

                for pos in range(input_start + len(self.buffer[found_label]), input_end + 1):
                    line_list[pos] = "_"

                line = "".join(line_list)

                if found_label == self.label:
                    label_start = line.find(found_label)
                    label_end   = label_start + len(found_label)
                    line        = bold(line, start=label_start, end=label_end)

            print(line, end="")


    def parse_keypress(self, key: str):
        response = -1 
        self.buffer_position[self.label] = max(self.buffer_position[self.label], 0)
        self.buffer_position[self.label] = min(self.buffer_position[self.label], 31)
        
        print(key)

        if key == "space":
            key = " "

        if key == "up":
            self.radio_selection -= 1 
            if self.radio_selection == -1:
                self.radio_selection = self.radio_selection_size - 1     

        elif key == "down":
            self.radio_selection += 1
            if self.radio_selection == self.radio_selection_size:
                self.radio_selection = 0

        elif key == "enter":
            self.parse_entered_values()
            response = "validate sign up"
            
        elif key in PERMITTED_CHARS:
            pos = self.buffer_position[self.label]
            if pos < 32:
                self.buffer[self.label][pos] = key
                self.buffer_position[self.label] += 1

        elif key == "backspace":
            pos = self.buffer_position[self.label]
            if pos >= 0:
                self.buffer[self.label][pos] = "_"
                self.buffer_position[self.label] -= 1
    
        self.label = self.data["OPTIONS"][self.radio_selection]
        # self.input_placeholder = "!" if self.label == "Username" else "$"
        return response

    def load_placeholder(self):
        placeholder_prompt = PlaceholderPrompt("placeholder", "data\\prompts\\ui\\placeholder.txt")
        return placeholder_prompt
    
    def tidy_up_key(self, key: str) -> str:
        key = key.lower()
        key = key.replace(" ", "_")
        return key

    def parse_entered_values(self):
        new_entered_values = {}
        for key in self.data["OPTIONS"]:
            new_key = self.tidy_up_key(key)
            new_entered_values[new_key] = "".join(self.buffer[key]).split("_")[0]

        self.entered_values = new_entered_values