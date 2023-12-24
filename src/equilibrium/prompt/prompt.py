from utils.parser import parse_txt_line
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv()
PATH_PROMPT_METADATA = os.getenv("PATH_PROMPT_METADATA")
PATH_PROMPT_UI       = os.getenv("PATH_PROMPT_UI")

class Prompt:
    def __init__(self, prompt_name: str):
        self.data_path = project_root / "data/prompts/metadata" / f"{prompt_name}.txt"
        self.ui_path   = project_root / "data/prompts/ui"       / f"{prompt_name}.txt"
        self.parse_data()

    def parse_data(self):
        data_file = open(self.data_path) # Open file 
        lines = data_file.readlines()    # Read file

        self.data = {}

        for line in lines: # Parse lines
            key, value = parse_txt_line(line)
            self.data[key] = value

        self.data["OPTIONS"] = self.data["OPTIONS"].split(",")
        self.radio_selection_size = len(self.data["OPTIONS"])    