def bold(text: str, start=0, end=-1) -> str:
    """
    Bolds text, given the first and the last position inside the string.
    
    Parameters
    ----------
    text : str
        Text to be formatted.
    start : int
        Starting position of the effect.
        Defaults to 0, meaning that the beginning was not provided and 
        the effect is to be applied from the begginning of the string.
    end : int
        Ending position of the effect.
        Defaults to -1, meaning that the end was not provided and the effect
        is to be applied until the end of the string.
        
    Returns
    -------
    str:
        Formatted string, as already described.
    """
    if end == -1: # If the end is not provided
        end = len(text) # End is the end of the string
    
    
    # Split string into three parts:
    # (1) Before the effect
    # (2) The effect itself
    # (3) After the effect
    
    # This way, it's easy to use f-strings to place "before" (1) and "after" (2)
    # parts into their spots, and also print necessary characters to modify
    # the "main" part (2)
    to_main_part = text[0:start] 
    main_part = text[start:end]
    from_main_part = text[end:]

    bolded_text = f"{to_main_part}\x1b[1;03;31m{main_part}\x1b[0m{from_main_part}"
    return bolded_text

def make_line(character: chr, length: int):
    return (character * length)

def clear_screen():
    """
    Clears the screen by printing a standard character / expression.
    """
    print("\033[H\033[J")