from .prompt import Prompt
from .login_prompt import LoginPrompt

import os
from dotenv import load_dotenv

load_dotenv()

PERMITTED_CHARS = os.getenv("PERMITTED_CHARS") 

class AddNewArticlePrompt(Prompt):
    def __init__(self, prompt_name: str):
        """
        Initialize a new instance of AddNewArticlePrompt.

        Parameters
        ----------
        - prompt_name : str
            Name of the AddNewArticlePrompt to be created. 
        """
        super().__init__(prompt_name)

        self.radio_selection      = 0 # Current radio button selection
        self.radio_selection_size = len(self.data["OPTIONS"]) 
        self.input_placeholder = "!"        # Placeholder for "Username" is "!"
        self.label             = "Title" # Starting field is "Username"
        
        # Dictionary of placeholders. 
        # Each placeholder is responsible for either being empty, or
        # containing an inputted character.
        self.placeholder = {"Title":   "!",
                            "Tags":    "$",
                            "Content": "^"
                           }
        
        # Buffers for each input field. 
        # Only "Date" field is 10 characters long, because of its format
        self.buffer = {"Title":   ["_"] * 70, 
                       "Tags":    ["_"] * 70,
                       "Content": [["_" for _ in range(120)] for _ in range(20)]
                       #"Content": ["_"] * (20 * 120)
                       }
        
        # Dictionary holding the current position within the input field.
        self.buffer_position = {"Title":   0, 
                                "Tags":    0,
                                "Content": (0, 0)
                               }
        
        # To be parsed later (entered values when "ENTER" is pressed)
        self.entered_values = {"Title":   "",
                               "Tags":    "",
                               "Content": ""
                              }
        
        self.newline_positions = []
        
        # After hitting "ENTER", user goes to PLACEHOLDER
        self.next_prompt = LoginPrompt("login")


    def show(self):
        """
        Show the current state of prompt.
        """
        ui = open(self.ui_path, encoding="utf8") # Open the User Interface
        
        lines = ui.readlines()
        
        lines = [line.strip() for line in lines]
        two_d_matrix =  [list(line) for line in lines]
        
        label_row       = 0
        label_col_start = 0
    
        input_row_start = 0
        input_col_start = 0
        
        input_row = 0
        input_col = 0
    
        # Title
        col_counter = 0
        for col in range(17, 87):
            two_d_matrix[3][col] = self.buffer["Title"][col_counter] 
            col_counter += 1
        
        if self.label == "Title":
            label_row = 3
            label_col_start = 6
            label_col_end   = 13
            
            input_row_start = 3
            input_col_start = 17
            
            input_row = 3
            input_col = input_col_start + self.buffer_position["Title"]
        
        # Tags
        col_counter = 0
        for col in range(17, 87):
            two_d_matrix[6][col] = self.buffer["Tags"][col_counter] 
            col_counter += 1
        
        if self.label == "Tags":
            label_row = 6
            label_col_start = 6
            label_col_end   = 10
            
            input_row_start = 6
            input_col_start = 17
            
            input_row = 6
            input_col = input_col_start + self.buffer_position["Tags"]
        
        # Content
        row_counter = 0
        col_counter = 0
        for row in range(10, 30):
            col_counter = 0
            
            for col in range(17, 137):
                two_d_matrix[row][col] = self.buffer["Content"][row_counter][col_counter]
                col_counter += 1
                
            row_counter += 1
        
        if self.label == "Content":
            label_row = 10
            label_col_start = 6
            label_col_end   = 14
            
            input_row_start = 10
            input_col_start = 17
            
            input_row = input_row_start + self.buffer_position["Content"][0]
            input_col = input_col_start + self.buffer_position["Content"][1]
        
        
        if self.label == "SUBMIT":
            label_row = 32
            label_col_start = 70
            label_col_end   = 76    
            
            
        for row in range(len(two_d_matrix)):
            for col in range(len(two_d_matrix[row])):
                if row == input_row and col == input_col:
                    print("\x1b[1;03;31m" + two_d_matrix[row][col] + "\x1b[0m", end="")
                
                elif row == label_row and label_col_start <= col and col <= label_col_end:
                    print("\x1b[1;03;31m" + two_d_matrix[row][col] + "\x1b[0m", end="")
                    
                else:
                    print(two_d_matrix[row][col], end="")
            
            print("")
        

    def parse_content_keypress(self, key: str) -> str:
        """
        Parses keypress hit specifically in the "Content" input, because
        it is 2-Dimensional.
        
        Parameters
        ----------
        key : str
            Key pressed while the SignUpPrompt was present - to be parsed.
        """
        
        row, col = self.buffer_position["Content"]
        
        response = ""
        
        if key == "space": 
            key = " "
            
           
        if key == "escape" or key == "esc":
            response = "load user profile"
        
        elif key == "up":
            row -= 1
            if row < 0:
                self.label = "Tags"
                # self.buffer_position["Content"] = (0, 0)
                
                
        elif key == "down":
            row += 1
            if row > 19:
                self.label = "SUBMIT"
                row = -1
                col = -1
                # self.buffer_position["Content"] = (0,0)
                
                
        elif key == "left":
            col -= 1
            if col < 0:
                col = 0
                
                
        elif key == "right":
            col += 1
            if col > 119:
                col = 119
                
            
        elif key in PERMITTED_CHARS: # If key is meaningful character for text
            self.buffer["Content"][row][col] = key    
            if col < 119: # If possible to enter text
                self.buffer["Content"][row][col] = key # Set the character
                col += 1 # Move one spot to the right
            elif col == 119:
                row += 1
                col = 0
                if row > 19:
                    row = 19
            
        elif key == "backspace":
            self.buffer["Content"][row][col] = "_"
            col -= 1
            if col < 0:
                col = 119
                row -= 1
                if row < 0:
                    row = 0
            
            
        self.buffer_position["Content"] = (row, col)
        
        #print(self.buffer["Content"])
        #time.sleep(1)
        
        return response
    

    def parse_keypress(self, key: str) -> str:
        """
        Parses key hit while the AddNewArticlePrompt was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the AddNewArticlePrompt was present - to be parsed.
        
        Returns
        -------
        str:
            Response to the main loop.
        """
        
        if key == "enter":
            self.parse_entered_values()
            return "new article ready"
        
        if self.label == "Content":
            response = self.parse_content_keypress(key)
            return response
        
        elif self.label == "SUBMIT":        
            if key == "up":
                self.label = "Content"
                self.buffer_position["Content"] = (0, 0)        
        
        else:
            response = "" # Default response 
            
            # If buffer's position is negative,    then return it to 0
            # If buffer's position is overflowing, then return it back to the maximum
            self.buffer_position[self.label] = max(self.buffer_position[self.label], 0)
            self.buffer_position[self.label] = min(self.buffer_position[self.label], 
                                                   len(self.buffer[self.label]))
            
            if key == "space":
                key = " "
                
            if key == "escape" or key == "esc":
              response = "load user profile"  
    
            elif key == "up":
                self.radio_selection -= 1 # Move radio selection for one upwards
                if self.radio_selection == -1: # If there is nothing on top
                    # Move selection to the last possible field / on the end
                    self.radio_selection = self.radio_selection_size - 1   
    
            elif key == "down": # Similar to the "up" case
                self.radio_selection += 1
                if self.radio_selection == self.radio_selection_size:
                    self.radio_selection = 0
    
            elif key == "enter": # Finalize entered values
                if self.label == "SUBMIT":
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
        
        self.buffer["Title"] = "".join(self.buffer["Title"])
        new_entered_values["title"] = self.buffer["Title"].split("_")[0]
        new_entered_values["title"] = new_entered_values["title"].strip()
        
        self.buffer["Tags"] = "".join(self.buffer["Tags"])
        new_entered_values["tags"] = self.buffer["Tags"].split("_")[0].split(",")
        new_entered_values["tags"] = [tag.strip().lower() for tag in new_entered_values["tags"]]
            
        new_entered_values["content"] = "\n".join(["".join(row) for row in self.buffer["Content"]])
        new_entered_values["content"] = new_entered_values["content"].replace("_", " ")
        
        self.entered_values = new_entered_values