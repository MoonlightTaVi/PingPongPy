"""
Various utilities for CLI interaction.
"""
__version__ = "1.0.0"
__author__ = "MoonlightTaVi"



def ask(message: str) -> bool:
    """
    Prints a message to the console 
    and asks the user to type either 'y' or 'n'.
    Will keep asking until the answer is any of the two valid ones.

    Returns True if the user said "yes", False otherwise.
    """

    is_valid = False
    said_yes = False

    inp = ''
    while not is_valid:
        print(f'{message} (Y/n)', end='')
        inp = input(': ').lower()
        
        if inp == 'y':
            said_yes = True
        elif inp == 'n':
            said_yes = False
        else:
            continue

        is_valid = True
    
    return said_yes