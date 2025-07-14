from os.path import abspath, dirname
from json import load, loads

from demo_assets.scripts.classic_mode import classicMode
from demo_assets.scripts.console import Console

try:
    if __name__ == "__main__":
        VERSION_NUMBER = 0.21  # Build version

        ## Assets

        # Lang objects
        with open(abspath(f"{dirname(__file__)}/demo_assets/lang/console_format_codes.json")) as f:
            FORMAT_CODES = load(f)
        con: Console = Console(FORMAT_CODES)
        with open(abspath(f"{dirname(__file__)}/demo_assets/lang/en.json")) as f:
            LANG: dict = loads(con.format_text(f.read()).replace("{ver}", str(VERSION_NUMBER)), strict=False)

        # Decks
        with open(abspath(f"{dirname(__file__)}/data/classic_deck.json")) as f:
            CLASSIC_DECK = load(f)

        # Main Program Loop
        loop = True
        while loop:
            # con.clear()  # screen clears on each iteration of loop

            boot = input(f"""
{LANG['new_line']}{LANG['main_menu_title']}
{LANG['new_line']}
{LANG['new_line']}1. {LANG['main_menu_01']}
{LANG['new_line']}2. {LANG['main_menu_02']}
{LANG['new_line']}Q. {LANG['main_menu_03']}
{LANG['new_line']}
{LANG['user_input']}""")
            match boot.lower():  # decodes user's input choice, refreshing the screen on invalid entry
                case "2" | "two":
                    n = input(classicMode(con, CLASSIC_DECK, LANG))
                    match n.lower():
                        case "q" | "quit": loop = False
                case "q" | "quit":
                    loop = False
                case _:
                    con.clear()

        con.clear()
        exit()  # end of program

except Exception as e:
    import sys
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        ...
        # with open("debug.txt", "w") as f:
        #     f.write(str(e))
    else:
        print(e)
