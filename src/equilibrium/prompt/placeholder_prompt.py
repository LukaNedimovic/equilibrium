from .prompt import Prompt

class PlaceholderPrompt(Prompt):
    def __init__(self, prompt_name: str):
        super().__init__(prompt_name)

        self.next_prompt = None

    def show(self):
        ui = open(self.ui_path, encoding="utf8")
        lines = ui.readlines()
        for line in lines:
            print(line, end="")