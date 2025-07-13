from random import shuffle
from json import loads, dumps
import os

VERSION_NUMBER = 0.1


# Class to handle ANSI escape codes
class Console:
    def __init__(self):
        self.black = "\033[0;30m"
        self.red = "\033[0;31m"
        self.green = "\033[0;32m"
        self.brown = "\033[0;33m"
        self.blue = "\033[0;34m"
        self.purple = "\033[0;35m"
        self.cyan = "\033[0;36m"
        self.light_gray = "\033[0;37m"
        self.dark_gray = "\033[1;30m"
        self.light_red = "\033[1;31m"
        self.light_green = "\033[1;32m"
        self.yellow = "\033[1;33m"
        self.light_blue = "\033[1;34m"
        self.light_purple = "\033[1;35m"
        self.light_cyan = "\033[1;36m"
        self.light_white = "\033[1;37m"
        self.bold = "\033[1m"
        self.faint = "\033[2m"
        self.italic = "\033[3m"
        self.underline = "\033[4m"
        self.blink = "\033[5m"
        self.negative = "\033[7m"
        self.crossed = "\033[9m"
        self.reset = "\033[0m"

    def colour(self, text, code):  # returns text with colour
        colour_code = getattr(self, code.lower(), '')
        return f"{colour_code}{text}{self.reset}"

    def card(self, card):  # returns card as coloured string
        match card[0]:  # gets colour for card value
            case 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10:
                value = f"{self.brown}{card[0]}"
            case 11:
                value = f"{self.light_green}J"
            case 12:
                value = f"{self.light_purple}Q"
            case 13:
                value = f"{self.light_blue}K"
            case 14:
                value = f"{self.bold}A"
            case _:
                value = f"{self.cyan}{card[0]}"
        match card[1]:  # gets colour for card suit
            case "H" | "D":
                suit = f"{self.light_red}{card[1]}"
            case "S" | "C":
                suit = f"{self.black}{self.bold}{card[1]}"
            case _:
                suit = f"{self.light_white}{card[1]}"

        # Returns card as formatted string with colour
        return f"{value}{self.reset}{suit}{self.reset}"

    def clear(self):
        print(self.reset)
        os.system('cls' if os.name == 'nt' else 'clear')


# Class to handle Classic ruleset - deck, room size and max health can still be changed for Classic+ rulesets
class ClassicGame:
    def __init__(self, deck, room_size=4, max_health=20):
        self.deck = deck  # classic rules use a standard deck, with all red face cards removed
        self.room = []
        self.discard_pile = []

        self.weapon = (0, 30)  # weapon = (damage, last monster killed)/  30 means no last monster killed

        self.room_size = room_size
        self.win_condition = 0
        self.player_health = self.player_max_health = max_health
        self.skip_count = 0
        self.heal_count = 0

        shuffle(self.deck)
        self.GetNextRoom()  # draws first room

    # Handles game overs
    def GameOver(self, code):
        self.win_condition = code
        return code

    # Draws the next room in the dungeon
    def GetNextRoom(self):
        # Check if deck is empty, if so player wins upon draw
        if len(self.deck) < self.room_size - 1: return self.GameOver(1)

        shuffle(self.deck)
        while len(self.room) < self.room_size:  # draws cards until room is filled up
            self.room.append(self.deck.pop())

        # resets skip and heal count on each new draw
        self.skip_count = 0
        self.heal_count = 0

        return 4

    def SkipRoom(self):
        if self.skip_count: return -1  # guard clause, stops player from skipping 2 rooms in a row

        for i in range(len(self.room)): self.deck.append(self.room.pop())  # shuffles room back into deck
        self.GetNextRoom()  # draws new room

        self.skip_count = 1  # sets skip count

    # Handles adding / removing from player's health
    def ChangeHealth(self, amount, damage=True):
        if damage:  # damages player, checks for game over condition
            self.player_health = max(0, self.player_health - amount)
            if self.player_health <= 0: self.GameOver(-1)
        else:  # heals player, caps value at max health
            self.player_health += amount
            self.player_health = min(self.player_max_health, self.player_health)  # caps the player's health
            self.heal_count = 1  # sets the heal count, player can't heal more than once per turn

    # Loads a new weapon
    def ChangeWeapon(self, damage):
        self.weapon = (damage, 30)  #

    # Handles monster attacks and weapon logic
    def AttackMonster(self, monster_health):
        if self.weapon[0] == 0:
            damage = monster_health  # guard clause for no weapon, stops barehanded combat breaking

        elif self.weapon[1] > monster_health:  # only uses weapon if last monster was not weaker or same as current one
            damage = max(0, (monster_health - self.weapon[0]))
            self.weapon = (self.weapon[0], monster_health)

        else:  # otherwise player takes full damage
            damage = monster_health
        self.ChangeHealth(damage)

    # Discards chosen card, plays its effects
    def PlayCard(self, card):
        self.discard_pile.append(self.room.pop(self.room.index(card)))  # moves card to discard pile

        match card[1]:
            case "H":  # hearts heal player, can only use one per turn
                if not self.heal_count: self.ChangeHealth(card[0], damage=False)
            case "D":  # diamonds are weapons, can only equip one
                self.ChangeWeapon(card[0])
            case "C" | "S":  # black cards are monsters, they deal damage equal to their face value
                self.AttackMonster(card[0])


# Print the rules for classic mode
def ClassicRules(con):
    con.clear()
    input(f"""
    >  {con.blue}{con.bold}{con.underline}CLASSIC MODE{con.reset} Rules (page {con.cyan}1{con.reset} of {con.red}2{con.reset})
    >
    >  {con.blue}Classic mode{con.reset} is played with a standard deck of cards (the {con.dark_gray}Dungeon{con.reset}). The {con.red}Jok{con.black}ers{con.reset} 
    >  and {con.red}Red Face Cards{con.reset} are removed from play.
    >  The game starts with {con.cyan}4{con.reset} cards turned over - this is called a {con.dark_gray}Room{con.reset}. To move to the next {con.dark_gray}Room{con.reset},
    >  you must either face {con.cyan}3{con.reset} of the {con.cyan}4{con.reset} cards present, or {con.purple}Skip{con.reset} the {con.dark_gray}Room{con.reset}. You cannot {con.purple}Skip{con.reset} more then
    >  {con.cyan}1{con.reset} {con.dark_gray}Room{con.reset} per turn. The goal is to beat every {con.dark_gray}Room{con.reset} in the {con.dark_gray}Dungeon{con.reset}.
    > {con.light_cyan}
    >  Press {con.reset}[ENTER]{con.light_cyan} to view the next page.{con.reset}""")
    con.clear()
    input(f"""
    >  {con.blue}{con.bold}{con.underline}CLASSIC MODE{con.reset} Rules (page {con.cyan}2{con.reset} of {con.red}2{con.reset})
    >
    >  {con.light_red}Hearts (H){con.reset} are {con.light_red}Potions{con.reset} that will {con.red}heal{con.reset} you for their face value.
    >  {con.light_red}Diamonds (D){con.reset} are {con.light_cyan}Weapons{con.reset} that attack for their face value.
    >  {con.dark_gray}Black cards (S) & (C){con.reset} are {con.dark_gray}Monsters{con.reset} cards that deal damage for their face value.
    >
    >  {con.light_cyan}Weapons{con.reset} dull as they are used, meaning you can only use it again on {con.dark_gray}Monsters{con.reset}
    >  that are {con.brown}weaker{con.reset} then the last one it was used on.
    >  You can only {con.red}heal{con.reset} once per turn, a second or third {con.light_red}Potion{con.reset} will not have any effect.
    > {con.light_cyan}
    >  Press {con.reset}[ENTER]{con.light_cyan} to return.{con.reset}""")


# Text-based version of classic mode
def ClassicMode(con):
    con.clear()
    menu = input(f"""
    >  Welcome to {con.yellow}Classic Scoundrel{con.light_cyan} v{VERSION_NUMBER}{con.reset}
    > 
    >  1. {con.light_green}Play{con.reset}
    >  2. {con.red}Rules{con.reset}
    >  Q. {con.dark_gray}Quit{con.reset}
    > {con.light_cyan}
    >  """)
    match menu.lower():
        case "1" | "one" | "play":
            pass
        case "2" | "two" | "rules":
            ClassicRules(con)
            return ClassicMode(con)
        case "q" | "quit":
            con.clear()
            return "thanks for playing"

    with open("classic_deck.json", "r") as f:
        deck = loads(f.read())
    game = ClassicGame(deck)

    game_loop = True
    while game_loop:
        # Sets skip count if card is played, resets upon draw
        if len(game.room) < 4: game.skip_count = 1

        # Replaces empty spaces with visual markers - avoids indexing errors
        from copy import copy
        current_room = copy(game.room)
        while len(current_room) < 4:
            current_room.append("<>")

        # Draws the new board
        con.clear()
        inp = input(f"""
    >  {con.yellow}Classic Scoundrel{con.reset}
    >  
    >  Cards Remaining:  >{con.green}{len(game.deck)}{con.reset}<
    >  1.  {con.card(current_room[0])}    2.  {con.card(current_room[1])}    3.  {con.card(current_room[2])}   4.  {con.card(current_room[3])}
    >  S.  {con.underline if not game.skip_count else ""}SKIP{con.reset}   Q.  {con.underline}{con.bold}QUIT{con.reset}
    >  
    >  {con.green}Health{con.reset}: >{con.light_red}{game.player_health}{con.reset}< | {con.green}Weapon{con.reset}: >{con.cyan}{game.weapon}{con.reset}<
    {con.light_cyan}>  """)
        # Processes player input
        match inp.lower():
            case "1" | "one":
                if current_room[0] != "<>": game.PlayCard(game.room[0])
            case "2" | "two":
                if current_room[1] != "<>": game.PlayCard(game.room[1])
            case "3" | "three":
                if current_room[2] != "<>": game.PlayCard(game.room[2])
            case "4" | "four":
                if current_room[3] != "<>": game.PlayCard(game.room[3])
            case "s" | "skip":
                game.SkipRoom()
            case "q" | "quit":
                game_loop = False

        # If the room is down to one card, next room is drawn
        if len(game.room) < 2: game.GetNextRoom()
        # Checks for win condition, ends game loop if so
        if game.win_condition != 0: game_loop = False

    con.clear()

    # Checks for win conditions
    if game.win_condition > 0:
        return "you won"
    elif game.win_condition < 0:
        return "you lost"
    else:
        return "thanks for playing"


if __name__ == "__main__":
    con = Console()
    con.clear()
    print(f"    >  {con.yellow}{con.underline}Scoundrel{con.reset} Card Game {con.cyan}v{VERSION_NUMBER}{con.reset}  -  {con.brown}Text Version{con.reset}")
    loop = True

    while loop:
        boot = input(f"""
    >
    >  1. {con.light_green}Play Classic Scoundrel{con.reset}
    >  E. {con.red}Exit Program{con.reset}
    > {con.light_cyan}
    >  """)
        match boot.lower():
            case "1" | "one":
                loop = False
                input(ClassicMode(con))
            case "e" | "exit":
                loop = False
            case _:
                con.clear()

    con.clear()
    exit()
