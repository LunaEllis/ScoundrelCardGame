## region Imports

# Script Imports
from resource_handler import *
from settings import *
from animations import *
from card import *
from dungeon import *
from menu import *

# Generic Imports
import sys
import ctypes
import pygame
import pygame.freetype

# Specific Imports
...

# endregion

## region Program Code

# Ignore resolution scaling
ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):
        ...

# endregion


if __name__ == '__main__':
    game = Game()
