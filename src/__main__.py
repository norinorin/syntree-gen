from PIL import Image, ImageDraw

from src.cli import ARGS
from src.config import BG_COLOUR
from src.draw import draw_nodes
from src.parser_ import Parser

buffer = []
text = "Type in the sentence (hit enter twice): "
while 1:
    if (temp := input(text)) == "":
        break

    buffer.append(temp)
    text = ": "

print("\nPlease wait...")

parser = Parser("".join(buffer))
node = parser.get_first_parent()
nodes, size = node.calculate_and_get_nodes()
out = Image.new("RGB", size, BG_COLOUR)
d = ImageDraw.Draw(out)
draw_nodes(nodes, d)

# TODO: cli & draw larger so it doesn't affect the size of the resulting image
out.resize((size[0] // 2, size[1] // 2), resample=Image.LANCZOS)

if ARGS.path:
    print("Saving to", ARGS.path)
    out.save(ARGS.path)

out.show()
print("Done!")
