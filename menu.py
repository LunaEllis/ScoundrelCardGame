# region IMPORTS AND TYPE DECLARATIONS
import pygame
import pygame.freetype

## Custom Type Declarations
# Type(Some Class)
type function = function
type Font = pygame.freetype.Font
type Rect = pygame.Rect
type Surface = pygame.Surface

# Type(Some Iterable)
type Pos = tuple[int, int]
type RGB = tuple[int, int, int]
type RGBA = tuple[int, int, int, int]
## endregion


## Custom Exceptions
class MenuObjectError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Text:
    def __init__(self):
        ...


class Button:
    def __init__(self):
        ...


class Image:
    def __init__(self):
        ...


class Menu:
    def __init__(self):
        ...


## Example Code
if __name__ == '__main__':
    ...
