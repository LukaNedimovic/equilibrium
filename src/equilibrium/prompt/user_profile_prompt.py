from .prompt import Prompt
from utils.formatting import bold

class UserProfilePrompt(Prompt):
    def __init__(self, prompt_name: str):
        """
        Initialize a new instance of UserProfilePrompt.
    
        Parameters
        ----------
        - prompt_name : str
            Name of the UserProfilePrompt to be created. 
        """
        super().__init__(prompt_name)

        self.radio_selection = 1 # Current radio button selection
        self.radio_selection_size = len(self.data["OPTIONS"])
        
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
            # For example, it creates: (1), (2), (3)...
            if f"({self.radio_selection})" in line:
                # Bold the selection
                line = bold(line, start=1, end=len(line)-2)
                
            print(line, end="")


    def parse_keypress(self, key: str) -> str:
        """
        Parse keypress hit while the UserProfilePrompt was present.
        
        Parameters
        ----------
        key : str
            Key pressed while the UserProfilePrompt was present - to be parsed.
        
        Returns
        -------
        str:
            Response to the main loop.
        """
        response = "" # Default response

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
            function_selected = self.data["OPTIONS"][self.radio_selection - 1]
            response = function_selected
            
        elif key == "tab":
            response = "terminate"
            
        return response
