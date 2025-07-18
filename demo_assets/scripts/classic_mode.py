from random import shuffle

from demo_assets.scripts.console import Console


# Console Screens
CLASSIC_GAME_TEXT = """
{new_line}{classic_game_title}
{new_line}
{new_line}{classic_game_01}
{new_line}{classic_game_02}
{new_line}{classic_game_03}
{new_line}
{new_line}{classic_game_04}
{user_input}"""

CLASSIC_RULES_01 = """
{new_line}{classic_rules_title}
{new_line}
{new_line}{classic_rules_01}
{new_line}{classic_rules_02}
{new_line}{classic_rules_03}
{new_line}{classic_rules_04}
{new_line}{classic_rules_05}
{new_line}
{user_input}{classic_rules_end}"""
CLASSIC_RULES_02 = """
{new_line}{classic_rules_title}
{new_line}
{new_line}{classic_rules_06}
{new_line}{classic_rules_07}
{new_line}{classic_rules_08}
{new_line}
{new_line}{classic_rules_09}
{new_line}{classic_rules_10}
{new_line}{classic_rules_11}
{new_line}
{user_input}{classic_rules_end}"""

CLASSIC_MENU = """
{new_line}{classic_menu_title}
{new_line}
{new_line}1. {classic_menu_01}
{new_line}2. {classic_menu_02}
{new_line}Q. {classic_menu_03}
{new_line}
{user_input}"""

CLASSIC_END_WIN = """
{new_line}{classic_end_menu_win}
{new_line}
{new_line}1. {classic_end_menu_01}
{new_line}Q. {classic_end_menu_02}
{new_line}
{user_input}"""
CLASSIC_END_LOSE = """
{new_line}{classic_end_menu_lose}
{new_line}
{new_line}1. {classic_end_menu_01}
{new_line}Q. {classic_end_menu_02}
{new_line}
{user_input}"""
CLASSIC_END_QUIT = """
{new_line}{classic_end_menu_quit}
{new_line}
{new_line}1. {classic_end_menu_01}
{new_line}Q. {classic_end_menu_02}
{new_line}
{user_input}"""


# Class to handle Classic ruleset - deck, room size and max health can still be changed for Classic+ rulesets
class ClassicGame:
    def __init__(self, deck: list[tuple], room_size: int = 4, max_health: int = 20):
        self.deck: list[tuple] = deck  # classic rules use a standard deck, with all red face cards removed
        self.room: list[tuple] = []
        self.discard_pile: list[tuple] = []

        self.weapon: list[int] = [0, 30]  # weapon = (damage, last monster killed)/  30 means no last monster killed

        self.room_size = room_size
        self.win_condition: int = 0
        self.player_health: int = max_health
        self.player_max_health: int = max_health
        self.skip_count: int = 0
        self.heal_count: int = 0

        shuffle(self.deck)
        self.GetNextRoom()  # draws first room

    # Handles game overs
    def GameOver(self, code: int) -> int:
        self.win_condition = code
        return code

    # Draws the next room in the dungeon
    def GetNextRoom(self) -> int:
        # Check if deck is empty, if so player wins upon draw
        if len(self.deck) < self.room_size - 1: return self.GameOver(1)

        shuffle(self.deck)
        while len(self.room) < self.room_size:  # draws cards until room is filled up
            self.room.append(self.deck.pop())

        # resets skip and heal count on each new draw
        self.skip_count = 0
        self.heal_count = 0

        return 4

    def SkipRoom(self) -> None:
        if self.skip_count: return  # guard clause, stops player from skipping 2 rooms in a row

        for i in range(len(self.room)): self.deck.append(self.room.pop())  # shuffles room back into deck
        self.GetNextRoom()  # draws new room

        self.skip_count = 1  # sets skip count

    # Handles adding / removing from player's health
    def ChangeHealth(self, amount: int, damage: bool = True) -> None:
        if damage:  # damages player, checks for game over condition
            self.player_health = max(0, self.player_health - amount)
            if self.player_health <= 0: self.GameOver(-1)
        else:  # heals player, caps value at max health
            self.player_health += amount
            self.player_health = min(self.player_max_health, self.player_health)  # caps the player's health
            self.heal_count = 1  # sets the heal count, player can't heal more than once per turn

    # Loads a new weapon
    def ChangeWeapon(self, damage: int) -> None:
        self.weapon = (damage, 30)  #

    # Handles monster attacks and weapon logic
    def AttackMonster(self, monster_health: int) -> None:
        if self.weapon[0] == 0:
            damage = monster_health  # guard clause for no weapon, stops barehanded combat breaking

        elif self.weapon[1] > monster_health:  # only uses weapon if last monster was not weaker or same as current one
            damage = max(0, (monster_health - self.weapon[0]))
            self.weapon = (self.weapon[0], monster_health)

        else:  # otherwise player takes full damage
            damage = monster_health
        self.ChangeHealth(damage)

    # Discards chosen card, plays its effects
    def PlayCard(self, card: tuple) -> None:
        self.discard_pile.append(self.room.pop(self.room.index(card)))  # moves card to discard pile

        match card[1]:
            case "H":  # hearts heal player, can only use one per turn
                if not self.heal_count: self.ChangeHealth(card[0], damage=False)
            case "D":  # diamonds are weapons, can only equip one
                self.ChangeWeapon(card[0])
            case "C" | "S":  # black cards are monsters, they deal damage equal to their face value
                self.AttackMonster(card[0])


# Print the rules for classic mode
def classicRulesText(con: Console, lang: dict) -> None:
    con.clear()
    input(CLASSIC_RULES_01.format(**lang).format(page=1,total=2))
    con.clear()
    input(CLASSIC_RULES_02.format(**lang).format(page=2,total=2))


# Text-based version of classic mode
def classicModeText(con: Console, deck: list[tuple], lang: dict) -> str:
    con.clear()
    menu = input(CLASSIC_MENU.format(**lang))
    match menu.lower():
        case "1" | "one" | "play":
            pass
        case "2" | "two" | "rules":
            classicRulesText(con, lang)
            return classicModeText(con, deck, lang)
        case "q" | "quit":
            con.clear()
            return CLASSIC_END_QUIT.format(**lang)

    game: ClassicGame = ClassicGame(deck)

    game_loop = True
    while game_loop:
        # Sets skip count if card is played, resets upon draw
        if len(game.room) < 4 and game.player_health > 0: game.skip_count = 1

        # Replaces empty spaces with visual markers - avoids indexing errors
        from copy import copy
        current_room = copy(game.room)
        while len(current_room) < 4:
            current_room.append(("<", ">"))

        # Draws the new board
        con.clear()
        inp = input(CLASSIC_GAME_TEXT.format(**lang).format(u=(con.underline if not game.skip_count else ""), deck=len(game.deck),
                                                            health=game.player_health, weapon=game.weapon,
                                                            c1=con.card(current_room[0]), c2=con.card(current_room[1]),
                                                            c3=con.card(current_room[2]), c4=con.card(current_room[3])))
        # Processes player input
        match inp.lower():
            case "1" | "one":
                if current_room[0] != ("<", ">"): game.PlayCard(game.room[0])
            case "2" | "two":
                if current_room[1] != ("<", ">"): game.PlayCard(game.room[1])
            case "3" | "three":
                if current_room[2] != ("<", ">"): game.PlayCard(game.room[2])
            case "4" | "four":
                if current_room[3] != ("<", ">"): game.PlayCard(game.room[3])
            case "s" | "skip":
                game.SkipRoom()
            case "q" | "quit":
                game_loop = False

        # If the room is down to one card, next room is drawn
        if len(game.room) < 2: game.GetNextRoom()
        # Checks for win condition, ends game loop if so
        if game.win_condition != 0: game_loop = False

    con.clear()

    # Checks game over conditions, loads the appropriate screen
    if game.win_condition > 0:
        return CLASSIC_END_WIN.format(**lang)
    elif game.win_condition < 0:
        return CLASSIC_END_LOSE.format(**lang)
    else:
        return CLASSIC_END_QUIT.format(**lang)
