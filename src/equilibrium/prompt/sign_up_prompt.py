from .prompt import Prompt
from .login_prompt import LoginPrompt
from .placeholder_prompt import PlaceholderPrompt

from utils.formatting import bold

import os
from dotenv import load_dotenv

load_dotenv()

PERMITTED_CHARS = os.getenv("PERMITTED_CHARS") 

class SignUpPrompt(Prompt):
    def __init__(self, prompt_name: str):
        """
        Initialize a new instance of SignUpPrompt.

        Parameters
        ----------
        - prompt_name : str
            Name of the SignUpPrompt to be created. 
        """
        super().__init__(prompt_name)

        self.radio_selection      = 0 # Current radio button selection
        self.radio_selection_size = len(self.data["OPTIONS"]) 
        self.input_placeholder = "!"        # Placeholder for "Username" is "!"
        self.label             = "Username" # Starting field is "Username"
        
        # Dictionary of placeholders. 
        # Each placeholder is responsible for either being empty, or
        # containing an inputted character.
        self.placeholder = {"Username":      "!",
                            "Password":      "$",
                            "Name":          "+",
                            "Surname":       "-",
                            "Date of birth": "^",
                            "Residence":     ",",
                            "Profession":    ";"}
        
        # Buffers for each input field. 
        # Only "Date" field is 10 characters long, because of its format
        self.buffer = {"Username":      ["_"] * 32, 
                       "Password":      ["_"] * 32,
                       "Name":          ["_"] * 32,
                       "Surname":       ["_"] * 32,
                       "Date of birth": ["_"] * 10,
                       "Residence":     ["_"] * 32,
                       "Profession":    ["_"] * 32}
        
        # Dictionary holding the current position within the input field.
        self.buffer_position = {"Username":      0, 
                                "Password":      0,
                                "Name":          0,
                                "Surname":       0,
                                "Date of birth": 0,
                                "Residence":     0,
                                "Profession":    0}
        
        # To be parsed later (entered values when "ENTER" is pressed)
        self.entered_values = {"Username":      "",
                               "Password":      "",
                               "Name":          "",
                               "Surname":       "",
                               "Date of birth": "",
                               "Residence":     "",
                               "Profession":    ""}
        
        # After hitting "ENTER", user goes to PLACEHOLDER
        self.next_prompt = LoginPrompt("login")


    def show(self):
        """
        Show the current state of prompt.
        """
        ui = open(self.ui_path, encoding="utf8") # Open the User Interface
        lines = ui.readlines()
        
        for line in lines: # Render prompt line by line
            
            # Check if there is any label present within the line   
            if any(label in line for label in self.data["OPTIONS"]):
                found_label = [label for label in self.data["OPTIONS"] 
                               if label in line][0] 
                input_placeholder = self.placeholder[found_label]

                # Find the borders of the input field
                input_start = line.find(input_placeholder) 
                input_end   = line.rfind(input_placeholder)

                # Turn the line into a list, making it mutable
                line_list   = [char for char in line] 
                
                # For respective position, set the corresponding character
                for pos in range(0, len(self.buffer[found_label])):
                    line_list[input_start + pos] = self.buffer[found_label][pos]

                # Remaining characters of the buffer are "_", nonetheless
                for pos in range(input_start + len(self.buffer[found_label]), input_end + 1):
                    line_list[pos] = "_"


                line = "".join(line_list) # Return line back to string

                # If found label is currently selected label
                if found_label == self.label:
                    label_start = line.find(found_label)
                    label_end   = label_start + len(found_label)
                    
                    # Apply "selected" effect to label
                    line        = bold(line, start=label_start, end=label_end)


            print(line, end="") # Show the line


    def parse_keypress(self, key: str) -> str:
        """
        Parse keypress hit while the SignUpPrompt was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the SignUpPrompt was present - to be parsed.
        
        Returns
        -------
        str:
            Response to the main loop.
            The only possible response, in right conditions,
            is "validate sign up".
        """
        
        response = -1 # Default response 
        
        # If buffer's position is negative,    then return it to 0
        # If buffer's position is overflowing, then return it back to the maximum
        self.buffer_position[self.label] = max(self.buffer_position[self.label], 0)
        self.buffer_position[self.label] = min(self.buffer_position[self.label], 
                                               len(self.buffer[self.label]) - 1)
        
        if key == "space":
            key = " "

        if key == "up":
            self.radio_selection -= 1 # Move radio selection for one upwards
            if self.radio_selection == -1: # If there is nothing on top
                # Move selection to the last possible field / on the end
                self.radio_selection = self.radio_selection_size - 1   

        elif key == "down": # Similar to the "up" case
            self.radio_selection += 1
            if self.radio_selection == self.radio_selection_size:
                self.radio_selection = 0

        elif key == "enter": # Finalize entered values
            self.parse_entered_values()   
            response = "validate sign up" # Response to the main loop updated
            
        elif key in PERMITTED_CHARS: # If key is meaningful character for text
            pos = self.buffer_position[self.label] # Get the position of buffer
            buffer_len = len(self.buffer[self.label])
            if pos < buffer_len: # If possible to enter text
                self.buffer[self.label][pos] = key # Set the character
                self.buffer_position[self.label] += 1 # Move one spot to the right

        elif key == "backspace": 
            pos = self.buffer_position[self.label] # Get the position of buffer
            if pos >= 0: # If there is anything to erase
                self.buffer[self.label][pos] = "_"    # Delete character
                self.buffer_position[self.label] -= 1 # Move one spot to the left
    
    
        # If selection has changed, then set another label as focused
        self.label = self.data["OPTIONS"][self.radio_selection] 
    
        return response # Return response to main loop
    

    def load_placeholder(self):
        placeholder_prompt = PlaceholderPrompt("placeholder", "data\\prompts\\ui\\placeholder.txt")
        return placeholder_prompt
    
    def tidy_up_key(self, key: str) -> str:
        """
        Convert key to lowercase and replace spaces with "-".
        
        Parameters
        ----------
        key : str
            Key in dictionary, to be tidied up, so it can be returned and parsed,
            later on nicely.
        
        Returns
        -------
        str
            Tidied up key, easier to be used and to avoid ambiguities.
        """
        key = key.lower()
        key = key.replace(" ", "_")
        
        return key
    

    def parse_entered_values(self):
        """
        Collect entered values in the form.
        Pack them so they can be returned in a nice format.
        """
        new_entered_values = {}
        for key in self.data["OPTIONS"]:
            new_key = self.tidy_up_key(key)
            new_entered_values[new_key] = "".join(self.buffer[key]).split("_")[0]

        self.entered_values = new_entered_values