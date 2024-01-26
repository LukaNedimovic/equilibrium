import keyboard
import sys

def capture_keypress():
    """
    Listen for keypresses and return the name of one after it has been pressed.
    
    Returns
    -------
    str:
        Name of the key pressed.

    """
    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        return event.name
    

def exit(): 
    """
    Function that termines program's execution.
    """
    sys.exit()