from src.font import get_font

# TODO: CLI arguments
CONTAINER_MARGIN = 50
TEXT_MARGIN = 50, 75
FONT_SIZE = 120
BG_COLOUR = "white"
END_COLOUR = "green"
LABEL_COLOUR = "blue"
LINE_COLOUR = "black"
LINE_WIDTH = 5
FONT_NAME = "Times New Roman"
FONT = get_font(FONT_NAME, FONT_SIZE)
HEIGHT_PER_DEPTH = sum(FONT.getmetrics())
