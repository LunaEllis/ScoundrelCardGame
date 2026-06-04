import pygame

from resource_handler import *
from settings import *
from card import *

from random import shuffle
from dataclasses import dataclass


@dataclass
class Player:
    health: int
    max_health: int
    weapon: CardBase | None = None
    inventory: list | None = None
    weapon_durability: int = 30
    run_flag = False
    potion_flag = False

    def add_health(self, value: int):
        if self.potion_flag: return

        self.health = min(self.max_health, self.health + value)
        self.potion_flag = True

    def remove_health(self, value: int):
        self.health -= max(0, value)

    def add_weapon(self, card: CardBase):
        self.weapon, self.weapon_durability = card, 30

    def draw_weapon(self, surface: Surface, pos: tuple[int, int]):
        if self.weapon: self.weapon.draw_to_surface(surface, pos)

    def attack_monster(self, value: int):
        if self.weapon and value <= self.weapon_durability:
            self.weapon_durability = value
            self.remove_health(value - self.weapon.get_value())

        else: self.remove_health(value)


class Dungeon:
    def __init__(self, name: str, **kwargs):
        dungeon = load_dungeon_from_file(name)

        self.name = dungeon['name']

        self.deck: list[CardBase] = []
        self.load_deck(dungeon['deck'])

        self.discard_pile: list[CardBase] = []

        self.room: list[CardBase] = []
        self.room_size: int = dungeon['room_size']
        self.room_topleft: tuple[int, int] = WIDTH // 5, Y_OFFSET + HEIGHT // 3

        self.player: Player = Player(**dungeon['player'])
        self.weapon_pos: tuple[int, int] = WIDTH // 8, Y_OFFSET + HEIGHT * 3 // 4

        self.ui_font = load_font("Exo-Regular.ttf", 32)
        self.ui_objects = {"health_pos": ((WIDTH // 2) - 200, Y_OFFSET + HEIGHT // 4),
                           "durability_pos": tuple(multiply(self.weapon_pos, (1, 0.9))),
                           'game_lost_1': self.ui_font.render("Game Over.", "red", size=72)[0],
                           'game_lost_2': self.ui_font.render("You Have Lost!", "red", size=72)[0],
                           'game_won_1': self.ui_font.render("Game Over.", "green", size=72)[0],
                           'game_won_2': self.ui_font.render("You beat the dungeon!", "green", size=72)[0],
                           'game_over_pos_1': (WIDTH//2, HEIGHT//2), 'game_over_pos_2': (WIDTH//2, (HEIGHT//2) + 80)}

        del dungeon

    def load_deck(self, card_list: list):
        for card in card_list:
            self.deck.append(CardBase(**card))
        load_card_images(self.deck)

    def shuffle_deck(self):
        shuffle(self.deck)

    def draw_card_from_deck(self, index=0):
        card = self.deck.pop(index)
        card.load_card_image()
        return card

    def populate_room(self):
        draw_size: int = max(0, self.room_size - len(self.room))

        for n in range(draw_size): self.room.append(self.draw_card_from_deck())

    def draw_room(self, surface: Surface):
        for card in self.room:
            offset = card.image.get_width() * 1.1 * self.room.index(card) + 1
            card.set_pos(tuple(add(self.room_topleft, (offset, 0))))

            card.draw_to_surface(surface, card.get_pos())

    def interact_with_card(self, mouse_pos, mouse_button):
        for card in self.room:
            if card.rect.collidepoint(mouse_pos):
                if mouse_button == pygame.BUTTON_LEFT: self.left_click_card(card)
                elif mouse_button == pygame.BUTTON_RIGHT: self.right_click_card(card)
                self.discard_from_room(card)

    def left_click_card(self, card: CardBase):
        match card.suit:
            case "H": self.player.add_health(card.get_value())
            case "D": self.player.add_weapon(card)
            case "C" | "S": self.player.attack_monster(card.get_value())

    def right_click_card(self, card: CardBase):
        ...

    def run_from_room(self):
        if self.player.run_flag: return

        self.player.run_flag = True
        self.player.potion_flag = False

        for card in self.room:
            self.deck.append(card)
            self.room.remove(card)
        self.shuffle_deck()
        self.populate_room()

    def discard_from_room(self, card: CardBase):
        self.discard_pile.append(card)
        self.room.remove(card)

    def discard_from_deck(self, index=0):
        self.discard_pile.append(self.draw_card_from_deck(index))

    def draw(self, surface: Surface):
        self.draw_room(surface)
        self.player.draw_weapon(surface, self.weapon_pos)

        surface.blit(self.ui_objects['health'], self.ui_objects['health_pos'])
        surface.blit(self.ui_objects['durability'], self.ui_objects['durability_pos'])

    def update(self):
        self.ui_objects['health'] = self.ui_font.render(f"Health: [{self.player.health} / {self.player.max_health}]",
                                                        BOOT_SCREEN_INSTRUCTIONS, size=32)[0]
        self.ui_objects['durability'] = self.ui_font.render(f"Weapon Durability: [{self.player.weapon_durability if 
                                                            self.player.weapon_durability <= 14 else "--"}]",
                                                            BOOT_SCREEN_INSTRUCTIONS, size=24)[0]

        if len(self.room) <= 1 and len(self.deck) >= 4:
            self.populate_room()
            self.player.run_flag = False
            self.player.potion_flag = False

        return self.game_over()

    def game_over(self):
        if self.player.health <= 0: return 1
        if len(self.room) < 1 and len(self.deck) < 4: return 2
        return 0


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION, DISPLAY_FLAGS)
    clock = pygame.time.Clock()

    font = Font(None, 32)

    d = Dungeon("default")
    d.shuffle_deck()
    d.populate_room()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                d.interact_with_card(event.pos, event.button)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE: break
                    case pygame.K_SPACE:
                        if len(d.room) == 4 and len(d.deck) >= 4:
                            d.run_from_room()
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill("black")

        game_over = d.update()
        if game_over > 0: break

        d.draw(screen)

        pygame.display.flip()
        clock.tick(FRAMERATE)

    screen.fill("black")

    match game_over:
        case 1: condition = "game_lost"
        case 2: condition = "game_won"
        # case _: condition = ""

    if f"{condition}_1" in d.ui_objects:
        rect_1 = d.ui_objects[f"{condition}_1"].get_rect()
        rect_1.center = d.ui_objects['game_over_pos_1']
        rect_2 = d.ui_objects[f"{condition}_2"].get_rect()
        rect_2.center = d.ui_objects['game_over_pos_2']
        screen.blit(d.ui_objects[f"{condition}_1"], rect_1)
        screen.blit(d.ui_objects[f"{condition}_2"], rect_2)

    pygame.display.flip()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN: run = False
            if event.type == pygame.MOUSEBUTTONDOWN: run = False

    pygame.quit()
