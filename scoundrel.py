import pygame

from os.path import abspath, dirname, relpath
from json import load, loads

from demo_assets.scripts.classic_mode import classicModeText
from demo_assets.scripts.console import Console


## Config
with open(abspath(f"{dirname(__file__)}/config.json"), "r") as a:
    CONFIG = load(a)
    VERSION_NUMBER = CONFIG['version-number']
    ASSETS = "assets" if not CONFIG['demo'] else "demo_assets"  # decodes which assets need to be loaded

## Assets


## Decks
with open(abspath(f"{dirname(__file__)}/data/standard_deck.json")) as deck1: STANDARD_DECK = load(deck1)
with open(abspath(f"{dirname(__file__)}/data/classic_deck.json")) as deck2: CLASSIC_DECK = load(deck2)


def textVersion():
    ## Language
    with open(abspath(f"{dirname(__file__)}/{ASSETS}/lang/console_format_codes.json")) as y:
        format_codes = load(y)
    con: Console = Console(format_codes)
    with open(abspath(f"{dirname(__file__)}/{ASSETS}/lang/en.json")) as z:
        lang: dict = loads(con.format_text(z.read()).replace("{ver}", str(VERSION_NUMBER)), strict=False)

    ## Console Screens
    menu_text = """
{new_line}{main_menu_title}
{new_line}
{new_line}1. {main_menu_01}
{new_line}2. {main_menu_02}
{new_line}Q. {main_menu_03}
{new_line}
{user_input}"""

    try:
        # Main Program Loop
        loop = True
        while loop:
            con.clear()  # screen clears on each iteration of loop

            boot = input(menu_text.format(**lang))
            match boot.lower():  # decodes user's input choice, refreshing the screen on invalid entry
                case "2" | "two":
                    n = input(classicModeText(con, CLASSIC_DECK, lang))
                    match n.lower():
                        case "q" | "quit": loop = False
                case "q" | "quit":
                    loop = False
                case _:
                    con.clear()

        con.clear()
        exit()  # end of program

    except Exception as e:  # 'Exception' needs to be replaced with list of common exceptions
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            with open("debug.txt", "w") as f:
                f.write(str(e))
        else:
            print(e)


def main():
    ...

try:
    if __name__ == '__main__':
        if CONFIG['text-based']: textVersion()
        else: main()
except BaseException as e:
    ...
    # with open(relpath("crash-log.txt"), "w") as f: f.write(str(e))
