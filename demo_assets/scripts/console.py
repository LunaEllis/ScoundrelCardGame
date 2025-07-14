from os import system, name
from re import sub


# Class to handle ANSI escape codes
class Console:
    def __init__(self, format_codes: dict = None):
        # Console text modifiers
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

        # If format code dictionary is passed through, it is stored. Else, empty dict is used.
        if format_codes is None: format_codes = {}
        self.format_codes: dict = format_codes

    # Adds colour codes to a string of text
    def colour(self, text: str, code: str) -> str:  # returns text with colour
        colour_code = getattr(self, code.lower(), '')
        return f"{colour_code}{text}{self.reset}"

    def card(self, card: tuple) -> str:  # returns card as coloured string
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

    def clear(self) -> None:
        print(self.reset)
        system('cls' if name == 'nt' else 'clear')

    # Formats any colour codes in strings (e.g. '#0' -> reset)
    def format_text(self, text: str) -> str:
        # First check is to remove percent escapes, and check for any colour codes. If there are none, text isn't processed
        result = sub("\\\\%", "{h//}", text)  # escaped percents are replaced with a marker
        if "%" not in result:
            return sub("{h//}", "%", result)  # markers are replaced with normal percents

        # Iterates through format code dictionary and replaces each colour code with corresponding value
        for code in self.format_codes:
            result = sub(str(code), self.format_codes[code], result)

        return result


if __name__ == "__main__":
    from json import loads
    with open("../lang/console_format_codes.json") as f:
        codes = loads(f.read())
    con = Console(codes)

    print(con.format_text("This text is normal. %bThis text is blue%0."))
