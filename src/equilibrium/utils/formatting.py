def bold(text: str, start=0, end=-1) -> str:
    if end == -1:
        end = len(text)
    
    to_main_part = text[0:start]
    main_part = text[start:end]
    from_main_part = text[end:]

    bolded_text = f"{to_main_part}\x1b[1;03;31m{main_part}\x1b[0m{from_main_part}"
    return bolded_text

def clear_screen():    
    print("\033[H\033[J")