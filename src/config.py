from src.font import get_font

# TODO: CLI arguments
CONTAINER_MARGIN = 50
TEXT_MARGIN = 50, 120
FONT_SIZE = 120
BG_COLOUR = "white"
END_COLOUR = "green"
LABEL_COLOUR_DEFAULT = ("black", "white")
LABEL_COLOURS = {
    # label bg text
    "S": ("orange", "white"),
    "V": ("blue", "white"),
    "VP": ("aqua", "white"),
    "N": ("red", "white"),
    "NP": ("green", "white"),
}
LABEL_MARGIN = 25
LINE_COLOUR = "black"
LINE_WIDTH = 8
LINE_MARGIN = 18
FONT_NAME = "Arial Unicode MS"
FONT = get_font(FONT_NAME, FONT_SIZE)
HEIGHT_PER_DEPTH = sum(FONT.getmetrics())


def get_label_colour(label):
    return LABEL_COLOURS.get(label, LABEL_COLOUR_DEFAULT)
