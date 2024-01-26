from utils.parser import parse_txt_line
from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv()
PATH_PROMPT_METADATA = os.getenv("PATH_PROMPT_METADATA")
PATH_PROMPT_UI       = os.getenv("PATH_PROMPT_UI")

class Prompt:
    def __init__(self, prompt_name: str):
        """
        Initialize a new instance of Prompt.

        Parameters
        ----------
        - prompt_name : str
            Name of the Prompt to be created. 
        """
        self.data_path = PROJECT_ROOT / "data/prompts/metadata" / f"{prompt_name}.txt"
        self.ui_path   = PROJECT_ROOT / "data/prompts/ui"       / f"{prompt_name}.txt"
        
        self.parse_data()

    def parse_data(self):
        """
        Parse data relevant to the Prompt.
        Additionally, add "OPTIONS", so it's known what user can select        
        """
        data_file = open(self.data_path, encoding="utf8") 
        lines = data_file.readlines()    

        self.data = {}

        for line in lines: # Parse lines
            key, value = parse_txt_line(line)
            self.data[key] = value

        self.data["OPTIONS"] = self.data["OPTIONS"].split(",")
        self.radio_selection_size = len(self.data["OPTIONS"])    