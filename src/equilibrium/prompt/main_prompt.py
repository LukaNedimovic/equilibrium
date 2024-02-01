from .prompt import Prompt
from .login_prompt import LoginPrompt
from .sign_up_prompt import SignUpPrompt
from utils.formatting import bold

import sys

class MainPrompt(Prompt):
    def __init__(self, prompt_name: str):
        """
        Initialize a new instance of MainPrompt.
    
        Parameters
        ----------
        - prompt_name : str
            Name of the MainPrompt to be created. 
        """
        super().__init__(prompt_name)

        self.radio_selection = 1 # Current radio button selection
        self.radio_selection_size = len(self.data["OPTIONS"])


        # Functionality associated with each option
        # Upon hitting "ENTER", object calls one of the associated functions.
        self.radio_selection_function = {1: self.login, 
                                         2: self.sign_up, 
                                         3: self.exit}
        
        # There is no set-in-stone next prompt,
        # since it only matters after choosing a singular option
        self.next_prompt = None


    def show(self):
        """
        Show the current state of prompt.
        """
        ui = open(self.ui_path, encoding="utf8") # Open the User Interface
        lines = ui.readlines()
        
        for line in lines: # Render prompt line by line
            # This format string is just a little cheat code.
            # It's used to create string with number among ().
            # For example, it's creates: (1), (2), (3)...
            if f"({self.radio_selection})" in line:
                # Bold the selection
                line = bold(line, start=1, end=len(line)-2)
                
            print(line, end="")

    def parse_keypress(self, key: str) -> str:
        """
        Parse keypress hit while the MainPrompt was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the MainPrompt was present - to be parsed.
        
        Returns
        -------
        str:
            Response to the main loop.
            The only possible response, in right conditions,
            is "load chosen option".
        """
        response = -1 # Default response

        if key == "up": 
            self.radio_selection -= 1 # Move radio selection for one upwards
            if self.radio_selection == 0: # If there is nothing on top
                # Move selection to the last possible field / on the end
                self.radio_selection = self.radio_selection_size     

        elif key == "down": # Similar to the "up" case
            self.radio_selection += 1
            if self.radio_selection == self.radio_selection_size + 1:
                self.radio_selection = 1

        elif key == "enter": # Open chosen option's prompt
            self.next_prompt = self.radio_selection_function[self.radio_selection]
            response = "load chosen option"
            
        return response


    def login(self) -> LoginPrompt:
        """
        Function to return a newly created MainPrompt.
        
        Returns
        -------
        LoginPrompt:
            New instance of MainPrompt class.
        """
        login_prompt = LoginPrompt("login")
        return login_prompt
    
    
    def sign_up(self) -> SignUpPrompt:
        """
        Function to return a newly created MainPrompt.
        
        Returns
        -------
        SignUpPrompt:
            New instance of MainPrompt class.
        """
        sign_up_prompt = SignUpPrompt("sign_up")
        return sign_up_prompt
    
    
    def exit(self): 
        """
        Function that termines program's execution.
        """
        sys.exit()