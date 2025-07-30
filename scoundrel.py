import pygame

from json import load, loads
from os.path import abspath, dirname
from PIL import Image

from demo_assets.scripts.menu import *
from demo_assets.scripts.text_version import main as text_version


## Config
with open(abspath(f"{dirname(__file__)}/config.json"), "r") as a:
    CONFIG = load(a)
    VERSION_NUMBER = CONFIG['version-number']
    ASSETS = "assets" if not CONFIG['demo'] else "demo_assets"  # decodes which assets need to be loaded

## Decks
with open(abspath(f"{dirname(__file__)}/data/standard_deck.json")) as deck1: STANDARD_DECK = load(deck1)
with open(abspath(f"{dirname(__file__)}/data/classic_deck.json")) as deck2: CLASSIC_DECK = load(deck2)


class Game:
    def __init__(self, config, assets, version, screen_size: tuple = (1280, 720)):
        ## PyGame Initialisation
        pygame.init()
        flags = 0
        self.screen = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption(f"Scoundrel v{version}")

        icon = Image.open("icon.ico")
        icon = icon.tobytes(), icon.size, icon.mode
        pygame.display.set_icon(pygame.image.frombytes(*icon))

        ## Asset Initialisation
        self.cards = ""

        ## Colour Initialisation
        self.black = (255, 0, 0, 0)
        self.white = (255, 255, 255, 255)

        ## Data initialisation
        ...

    def gameloop(self):
        ## Main Program
        run = True
        while run:
            ...

    def save_game(self):
        ...

    @staticmethod
    def quit():
        pygame.quit()
        return False


try:
    if __name__ == '__main__':
        if CONFIG['text-based']: text_version(VERSION_NUMBER, ASSETS, CLASSIC_DECK)
        else:
            game = Game(CONFIG, ASSETS, VERSION_NUMBER)
            game.gameloop()

except Exception as e:  # 'Exception' needs to be replaced with list of common exceptions
    # import sys
    #
    # if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    #     with open("debug.txt", "w") as f:
    #         f.write(str(e))
    # else:
    #     print(e)
    print(e)
