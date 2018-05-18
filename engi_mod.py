import utils
from spire import Card as card_func, Power as power_func, Action as action_func, Java as java_func
import os

cards = []
def Card(**kwargs):
    card = card_func(color="yellow", **kwargs)
    cards.append(card)
powers = []
def Power(**kwargs):
    power = power_func(**kwargs)
    powers.append(power)
actions = []
def Action(**kwargs):
    action = action_func(**kwargs)
    actions.append(action)
javas = []
def Java(**kwargs):
    java = java_func(**kwargs)
    javas.append(java)
WIP = lambda **kwargs: None

for file in utils.list_files("effects"):
    with open(os.path.join("effects", file), encoding="utf-8") as file:
        exec(file.read(), {})
for file in utils.list_files("cards"):
    with open(os.path.join("cards", file), encoding="utf-8") as file:
        exec(file.read(), {})

relic = "Art of War"

deck =\
    ["Strike_P"] * 4 +\
    ["Ammo Crate"] +\
    ["Defend_P"] * 5
if False:
    # deck += ["Combat Capsule", "Construction"] * 3
    deck = None
if False:
    deck =\
        ["Searing Blow"] * 4 +\
        ["Battle Trance"] * 2 +\
        ["Invent"] * 3 +\
        ["Armaments"]

keywords = {
    "Energize": {
        "words": [],
        "desc": "Draw an additional card and gain #b1 energy at the start of your next turn. Stacks duration.",
    },
    "Plated Armor": {
        "words": [],
        "desc": "Gain #yBlock at the end of your turn. Losing HP from an attack reduces #yPlated #yArmor by #b1.",
    }, # NOTE: doesn't work
}

__version__ = "0.1"

info = {
    "modid": "engimod",
    "name": "EngiMod",
    "author_list": ["Coft"],
    "description": "Adds the Engineer character.",
    "dependencies": ["basemod"],
    "version": __version__,
}
