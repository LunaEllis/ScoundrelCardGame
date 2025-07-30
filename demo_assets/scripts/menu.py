import pygame

## Custom Type Declarations
# Type(Some Class)
type function = function
type Font = pygame.font.Font
type Rect = pygame.Rect
type Surface = pygame.Surface

# Type(Some Iterable)
type Pos = tuple[int, int]
type RGB = tuple[int, int, int]
type RGBA = tuple[int, int, int, int]


## Custom Exceptions
class MenuObjectError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Text:
    def __init__(self, pos: Pos, text: str, font: Font, colour: RGBA) -> None:
        self.pos = pos
        self.font = font
        self.text = self.font.render(text, True, colour)
        self.rect = self.text.get_rect()
        self.rect.topleft = pos

    def draw(self, screen: Surface) -> None:
        screen.blit(self.text, self.rect)


class Button(Text):
    def __init__(self, pos: Pos, text: str, font: Font, colour: RGBA, func: function, image: Surface = None) -> None:
        super().__init__(pos, text, font, colour)

        self.func = func
        self.image = image
        if image:
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

    def draw(self, screen: Surface) -> None:
        if self.image:
            screen.blit(self.image, self.pos)
        super().draw(screen)

    def clicked(self) -> None:
        self.func()


class Menu:
    def __init__(self, name: str, screen: Surface, **fonts: Font) -> None:
        self.name = name
        self.screen = screen
        self.fonts = fonts

        self.objects = []

    def add_title(self, pos: Pos, text: str, colour: RGBA) -> None:
        if "title" not in self.fonts: raise MenuObjectError("Title Font not found.")
        self.objects.append(Text(pos, text, self.fonts['title'], colour))

    def add_header(self, pos: Pos, text: str, colour: RGBA) -> None:
        if "header" not in self.fonts: raise MenuObjectError("Header Font not found.")
        self.objects.append(Text(pos, text, self.fonts['header'], colour))

    def add_text(self, pos: Pos, text: str, colour: RGBA) -> None:
        if "text" not in self.fonts: raise MenuObjectError("Text Font not found.")
        self.objects.append(Text(pos, text, self.fonts['text'], colour))

    def add_button(self, pos: Pos, text: str, colour: RGBA, func: function, image: Surface = None) -> None:
        if "text" not in self.fonts: raise MenuObjectError("Text Font not found.")
        self.objects.append(Button(pos, text, self.fonts['text'], colour, func, image))

    def add_image(self, pos: Pos, image: Surface) -> None:
        self.screen.blit(image, pos)
        self.objects.append(image)

    def draw_menu(self) -> None:
        for obj in self.objects:
            if isinstance(obj, (Text, Button)): obj.draw(self.screen)

    def click_detection(self, mouse_pos: Pos):
        for obj in self.objects:
            if isinstance(obj, Button) and obj.rect.collidepoint(mouse_pos): obj.clicked()


if __name__ == '__main__':
    def prnt():
        print("button hath been pressed!!!")

    pygame.init()

    screen_obj = pygame.display.set_mode((1280, 720))

    title_font = pygame.font.Font(None, size=64)
    header_font = pygame.font.Font(None, size=48)
    text_font = pygame.font.Font(None, size=32)

    menu = Menu("menu", screen_obj, title=title_font, header=header_font, text=text_font)
    menu.add_title((10, 10), "Title Screen", (255, 255, 255, 255))
    menu.add_header((10, 60), "Header:", (255, 255, 255, 230))
    menu.add_text((10, 100), "Text block.", (255, 255, 255, 200))
    menu.add_button((300, 100), "Print!", (255, 255, 255, 200), prnt)

    menu.draw_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item in menu.objects: menu.click_detection(event.pos)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pygame.display.update()
