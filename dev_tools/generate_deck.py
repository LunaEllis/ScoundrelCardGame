from json import dump
from os import getcwd
from os.path import dirname

DIR = getcwd()
PARENT_DIR = dirname(DIR)


def populate_deck(suits, values, modifiers, image_file_needed=True):
    deck: list = []
    image = ""

    for suit in suits:
        for value in values:
            if image_file_needed: image = f"{value}{suit}.png"

            deck.append({"suit": suit, "value": value, "modifiers": modifiers, "image_file": image})

    return deck


deck_name = "default"
player = {"health": 20, "max_health": 20, "weapon": None, "inventory": None}
room_size = 4

number_suits = ["C", "H", "S", "D"]
face_suits = ["C", "S"]

number_values = ["2", "3", "4", "5", "6", "7", "8", "9", "T"]
face_values = ["J", "Q", "K", "A"]

card_modifiers = []

card_list = populate_deck(number_suits, number_values, card_modifiers) + populate_deck(face_suits, face_values, card_modifiers)

deck_dict = {
    "name": deck_name,
    "player": player,
    "room_size": room_size,
    "deck": card_list
}


with open(f"{PARENT_DIR}/dungeons/{deck_name}.json", "w") as f:
    dump(deck_dict, f)
print(deck_dict)
