from enum import Enum

class State(Enum):
    menu = 'm'
    set_deck = 's'
    playing = 'e'
    config = 'c'
    quit = 'q'

class Mode(Enum):
    bySets = 0
    sm2plus = 1
