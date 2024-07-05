import json

from src.cli import ARGS
from src.font import get_font

RECTANGLE_RADIUS = 25
CONTAINER_MARGIN = 50
TEXT_MARGIN = 50, 120
FONT_SIZE = 120
BG_COLOUR = "white"
END_COLOUR = "#3A3B3C"
LABEL_COLOURS = {}

with open(ARGS.colour_scheme or "default_colours.json", "r") as f:
    LABEL_COLOURS.update(json.load(f))

LABEL_COLOUR_DEFAULT = LABEL_COLOURS.pop("{default}", ("#ff7477", "white"))

LABEL_MARGIN = 25
LINE_COLOUR = "#3A3B3C"
LINE_WIDTH = 8
LINE_MARGIN = 18
FONT_NAME = "Dejavu Sans"
FONT = get_font(FONT_NAME, FONT_SIZE)
HEIGHT_PER_DEPTH = sum(FONT.getmetrics())


def get_label_colour(label):
    return LABEL_COLOURS.get(label, LABEL_COLOUR_DEFAULT)
