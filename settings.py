## A collection of useful data / settings for the program.
from pygame import SCALED, NOFRAME, RESIZABLE, FULLSCREEN

## Window data
WINDOW_TITLE = "ScoundrelRouge-like"
WINDOW_ICON_FILE = "icon.ico"
RESOLUTION = WIDTH, HEIGHT = 1366, 768
DISPLAY_FLAGS = SCALED | NOFRAME | RESIZABLE
FRAMERATE = 144

Y_OFFSET = 0 - (HEIGHT * 100 // 768)

## Assets and Program Data
AUDIO_DIR = ""
IMAGES_DIR = "images"
FONT_DIR = "fonts"
CARDS_DIR = "cards"
CARD_BACK_FILE = "cardBack_red2"

TITLE_SCREEN_FONT = "Exo-Medium.ttf"

## Colour Data
BOOT_SCREEN_BACKGROUND = (0, 0, 0, 255)
BOOT_SCREEN_TITLE = (87, 26, 9, 255)
BOOT_SCREEN_SUBTITLE = (92, 84, 82, 255)
BOOT_SCREEN_INSTRUCTIONS = (200, 200, 200, 255)


VALUE_TRANSLATIONS = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                      '8': 8, '9': 9}
