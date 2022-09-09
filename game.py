from enum import Enum
from colorama import Fore

class State(Enum):
    menu = 'm'
    set_deck = 's'
    playing = 'e'
    config = 'c'
    quit = 'q'

class Mode(Enum):
    bySets = 0
    sm2plus = 1

class Icon(Enum):
    WRONG = f'{Fore.RED}{Fore.RESET}'
    CORRECT = f'{Fore.GREEN}{Fore.RESET}'
    INPUT = '> '
    BOX_V = '│'
    BOX_H = '─'
    BOX_UL = '┌'
    BOX_UR = '┐'
    BOX_BR = '┘'
    BOX_BL = '└'

