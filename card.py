from resource_handler import *
from settings import *

from dataclasses import dataclass


@dataclass
class CardBase:
    suit: str
    value: str
    modifiers: list[str]
    image_file: str
    image: Surface = None
    rect: Rect = None

    def load_card_image(self):
        self.image = load_png(f"{CARDS_DIR}/{self.image_file}")[0]
        self.image = pygame.transform.scale(self.image, tuple(multiply(self.image.get_size(), (1.1, 1.1))))
        self.rect = self.image.get_rect()

    def get_value(self):
        return VALUE_TRANSLATIONS[self.value]

    def get_pos(self, point: str = "topleft"):
        match point:
            case "topleft": return self.rect.topleft
            case "midleft": return self.rect.midleft
            case "bottomleft": return self.rect.bottomleft
            case "midtop": return self.rect.midtop
            case "center": return self.rect.center
            case "midbottom": return self.rect.midbottom
            case "topright": return self.rect.topright
            case "midright": return self.rect.midright
            case "bottomright": return self.rect.bottomright

    def set_pos(self, pos: tuple, point: str = "topleft"):
        match point:
            case "topleft": self.rect.topleft = pos
            case "midleft": self.rect.midleft = pos
            case "bottomleft": self.rect.bottomleft = pos
            case "midtop": self.rect.midtop = pos
            case "center": self.rect.center = pos
            case "midbottom": self.rect.midbottom = pos
            case "topright": self.rect.topright = pos
            case "midright": self.rect.midright = pos
            case "bottomright": self.rect.bottomright = pos

    def draw_to_surface(self, surface: Surface, pos: tuple):
        surface.blit(self.image, pos)


def load_card_images(card_list: list[CardBase]):
    for card in card_list: card.load_card_image()
