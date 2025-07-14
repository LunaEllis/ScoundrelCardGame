from re import sub

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


con = Console()

print(con.colour("Hello ", "red"), con.colour("World!!", "light_red"))
print(f"""
List of colours:
{con.black}black{con.reset}
{con.red}red{con.reset}
{con.green}green{con.reset}
{con.brown}brown{con.reset}
{con.blue}blue{con.reset}
{con.purple}purple{con.reset}
{con.cyan}cyan{con.reset}
{con.light_gray}light_gray{con.reset}
{con.dark_gray}dark_gray{con.reset}
{con.light_red}light_red{con.reset}
{con.light_green}light_green{con.reset}
{con.yellow}yellow{con.reset}
{con.light_blue}light_blue{con.reset}
{con.light_purple}light_purple{con.reset}
{con.light_cyan}light_cyan{con.reset}
{con.light_white}light_wight{con.reset}
{con.bold}bold{con.reset}
{con.faint}faint{con.reset}
{con.underline}underline{con.reset}
{con.italic}italic{con.reset}
{con.blink}blink{con.reset}
{con.negative}negative{con.reset}
{con.crossed}crossed
{con.reset}reset""")