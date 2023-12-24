import keyboard

def capture_keypress():
    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        return event.name