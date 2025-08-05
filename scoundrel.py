# import pygame

from json import load, loads
from os.path import abspath, dirname

import pygame.font
from PIL import Image

from demo_assets.scripts.menu import *
from demo_assets.scripts.text_version import main as text_version

## Load Config
with open(abspath(f"{dirname(__file__)}/config.json"), "r") as a:
    CONFIG = load(a)
    VERSION_NUMBER = CONFIG['version-number']
    ASSETS = "assets" if not CONFIG['demo'] else "demo_assets"  # decodes which assets need to be loaded

## Load Decks
with open(abspath(f"{dirname(__file__)}/data/standard_deck.json")) as deck1: STANDARD_DECK = load(deck1)
with open(abspath(f"{dirname(__file__)}/data/classic_deck.json")) as deck2: CLASSIC_DECK = load(deck2)


def fade_animation(obj: Text | Button, fade: bool, step: int = 10):
    if fade: obj.fade_out(step)
    else: obj.fade_in(step)


class Game:
    def __init__(self, config: dict, assets: str, version: str, screen_size: tuple = (1280, 720)):
        ## Pygame Initialisation
        pygame.init()
        flags = 0
        self.screen: Surface = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption(f"Scoundrel v{version}")

        icon = Image.open("icon.ico")
        icon = icon.tobytes(), icon.size, icon.mode
        pygame.display.set_icon(pygame.image.frombytes(*icon))

        self.clock = pygame.time.Clock()
        self.framerate: int = 30

        ## Asset Initialisation
        self.cards = ""

        ## Colour Initialisation
        self.black: RGBA = (0, 0, 0, 255)
        self.white: RGBA = (255, 255, 255, 255)

        ## Font Initialisation
        self.title: Font = pygame.font.Font(None, 48)
        self.header: Font = pygame.font.Font(None, 32)
        self.text: Font = pygame.font.Font(None, 24)

        ## Data initialisation
        boot_menu = Menu("boot", self.screen, title=self.title, header=self.header,
                         text=self.text)

        self.current_gamestate: str = "boot_menu"
        self.gamestates: dict[str, Menu] = {self.current_gamestate: boot_menu}

    def gameloop(self):
        ## Boot Screen Initialisation
        self.boot_menu()
        boot_text_fade = True
        boot_text_obj: Text | Button = self.gamestates[self.current_gamestate].objects[0]

        run = True
        while run:
            ## Boot Screen
            if self.current_gamestate is "boot_menu":
                fade_animation(boot_text_obj, boot_text_fade, 5)
                if boot_text_obj.alpha <= 0: boot_text_fade = False
                elif boot_text_obj.alpha >= 255: boot_text_fade = True

            ## Start Menu
            ...

            ## Main Program
            ...

            ## Draws Screen
            self.draw_gamestate()

            ## Event Handler
            self.event_handler()

            ## Next Frame
            self.clock.tick(self.framerate)

    def save_game(self):
        ...

    def load_game(self):
        ...

    @staticmethod
    def quit():
        pygame.quit()
        quit()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.quit()

            if self.current_gamestate.endswith("menu"):
                if event.type == pygame.MOUSEBUTTONDOWN: self.click_event(event)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_menu()
                    return 1

    def click_event(self, event):
        try: self.gamestates[self.current_gamestate].click_detection(event.pos)
        finally: ...

    def boot_menu(self):
        # if the current gamestate points to a menu, load that menu; else, return
        menu = self.gamestates[self.current_gamestate] if self.current_gamestate.endswith("menu") else None
        if not menu: return -1

        menu.add_header((300, 600), "Press [SPACE] to begin...", self.white)

    def start_menu(self):
        self.current_gamestate = 'start_menu'
        menu = Menu('start_menu', self.screen, title=self.title, header=self.header, text=self.text)
        self.gamestates[self.current_gamestate] = menu

        menu.add_button((300, 300), "Quit!", self.white, self.quit)

    def draw_gamestate(self):
        self.screen.fill(self.black)  # clears screen

        self.gamestates[self.current_gamestate].draw_menu()

        pygame.display.flip()


try:
    if __name__ == '__main__':
        if CONFIG['text-based']:
            text_version(VERSION_NUMBER, ASSETS, CLASSIC_DECK)
        else:
            game = Game(CONFIG, ASSETS, VERSION_NUMBER)
            game.gameloop()

except Exception as e:  # 'Exception' needs to be replaced with list of common exceptions
    # import sys
    #
    # if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    #     with open("debug.txt", "w") as f: f.write(str(e))
    # else:
    #     print(e)
    print(e)
