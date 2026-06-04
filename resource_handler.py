from settings import *

import pygame
import pygame.freetype

from json import load as load_json
from os import getcwd
from os.path import join as join_path
from PIL.Image import open as pil_open
from numpy import multiply, divide, subtract, add
from pygame import Surface, Rect
from pygame.freetype import Font

# Locates program directory
PROGRAM_DIR: str = getcwd()

def filenotfounderror_handler(file_name: str, error: BaseException) -> None:
    """Generic FileNotFoundError handler"""
    print(f"File {file_name} could not be located in {PROGRAM_DIR}.")
    print(error)


def load_icon(file_name: str) -> pygame.Surface | pygame.SurfaceType:
    """Loads .ico file as a pygame Surface"""

    file_path: str = join_path(PROGRAM_DIR, file_name)

    try:
        icon_image = pil_open(file_path)
        icon_image = icon_image.tobytes(), icon_image.size, icon_image.mode

    except FileNotFoundError as error:
        filenotfounderror_handler(file_name, error)
        raise SystemExit

    return pygame.image.frombytes(*icon_image)


def load_png(file_name: str) -> (pygame.Surface | pygame.SurfaceType, pygame.Rect):
    """ Loads .png file as a pygame Surface."""

    file_path = join_path(PROGRAM_DIR, IMAGES_DIR, file_name)

    try:
        png_image = pygame.image.load(file_path)

        if png_image.get_alpha():
            png_image = png_image.convert_alpha()
        else:
            png_image = png_image.convert()

    except FileNotFoundError as error:
        filenotfounderror_handler(file_name, error)
        raise SystemExit

    return png_image, png_image.get_rect()


def load_font(name: str, size: int) -> pygame.freetype.Font:
    try:
        path = join_path(PROGRAM_DIR, FONT_DIR, name)
        font = pygame.freetype.Font(path, size)

    except FileNotFoundError as error:
        filenotfounderror_handler(name, error)
        raise SystemError

    return font


def load_dungeon_from_file(name: str) -> dict:
    with open(f"{PROGRAM_DIR}/dungeons/{name}.json", "r") as f:
        return load_json(f)
