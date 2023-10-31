from matplotlib import font_manager
from PIL import ImageFont


def get_font(name: str, size: int):
    return ImageFont.truetype(font_manager.findfont(name), size)
