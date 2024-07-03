from PIL import Image, ImageDraw

from src.cli import get_args
from src.config import BG_COLOUR
from src.draw import draw_nodes
from src.parser_ import Parser

args = get_args()
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

if args.path:
    print("Saving to", args.path)
    out.save(args.path)

out.show()
print("Done!")
