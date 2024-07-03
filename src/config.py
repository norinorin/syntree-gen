from src.font import get_font

# TODO: CLI arguments
RECTANGLE_RADIUS = 25
CONTAINER_MARGIN = 50
TEXT_MARGIN = 50, 120
FONT_SIZE = 120
BG_COLOUR = "white"
END_COLOUR = "#3A3B3C"
LABEL_COLOUR_DEFAULT = ("#ff7477", "white")
LABEL_COLOURS = {
    # label bg text
    "S": ("#845EC2", "white"),
    "V": ("#D65DB1", "white"),
    "VP": ("#FF6F91", "white"),
    "N": ("#FF9671", "white"),
    "NP": ("#FFC75F", "#3A3B3C"),
    "Adj": ("#F9F871", "#3A3B3C"),
    "AdjP": ("#bdb2ff", "#3A3B3C"),
    "Adv": ("#c1fba4", "#3A3B3C"),
    "C": ("#ffd972", "#3A3B3C"),
    "CP": ("#e8ffb7", "#3A3B3C"),
    "P": ("#e574bc", "white"),
    "PP": ("#f9b4ed", "#3A3B3C"),
}
LABEL_MARGIN = 25
LINE_COLOUR = "#3A3B3C"
LINE_WIDTH = 8
LINE_MARGIN = 18
FONT_NAME = "Dejavu Sans"
FONT = get_font(FONT_NAME, FONT_SIZE)
HEIGHT_PER_DEPTH = sum(FONT.getmetrics())


def get_label_colour(label):
    return LABEL_COLOURS.get(label, LABEL_COLOUR_DEFAULT)
