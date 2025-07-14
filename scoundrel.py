from os.path import abspath
from json import load

from demo_assets.scripts.classic_mode import classicMode
from demo_assets.scripts.console import Console

VERSION_NUMBER = 0.1  # Build version

## Assets

# Lang objects
with open(abspath("demo_assets/lang/format_codes.json")) as f:
    FORMAT_CODES = load(f)
with open(abspath("demo_assets/lang/en.json")) as f:
    MENU_TEXT = load(f)

# Decks
with open(abspath("data/classic_deck.json")) as f:
    CLASSIC_DECK = load(f)


if __name__ == "__main__":
    con: Console = Console()
    loop = True

    while loop:
        con.clear()  # screen clears on each iteration of loop

        boot = input(f"""
    >  {con.yellow}{con.underline}Scoundrel{con.reset} Card Game {con.cyan}v{VERSION_NUMBER}{con.reset}  -  {con.brown}Text Version{con.reset}
    >
    >  1. Scoundrel v{VERSION_NUMBER}
    >  2. {con.light_green}Classic Mode{con.reset}
    >  E. {con.red}Exit Program{con.reset}
    > {con.light_cyan}
    >  """)
        match boot.lower():  # decodes user's input choice, refreshing the screen on invalid entry
            case "2" | "two":
                n = input(classicMode(con, CLASSIC_DECK, MENU_TEXT, VERSION_NUMBER))
                match n.lower():
                    case "q" | "quit": loop = False
            case "e" | "exit":
                loop = False
            case _:
                con.clear()

    con.clear()
    exit()  # end of program
