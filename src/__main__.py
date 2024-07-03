from PIL import Image, ImageDraw

from src.cli import get_args
from src.config import *
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

for i, siblings in enumerate(nodes):
    for node in siblings:
        if node.is_label:
            d.rounded_rectangle(
                (
                    (node.x - LABEL_MARGIN, node.y - LABEL_MARGIN),
                    (
                        node.x + node.width + LABEL_MARGIN,
                        node.y + HEIGHT_PER_DEPTH + LABEL_MARGIN,
                    ),
                ),
                radius=25,
                fill=get_label_colour(node.text)[0],
            )
        d.text(
            (node.x, node.y),
            node.text,
            fill=get_label_colour(node.text)[1] if node.is_label else END_COLOUR,
            font=FONT,
        )
        if parent := node.parent:
            if parent.draws_triangle:
                p1 = (
                    parent.x + parent.width // 2,
                    parent.y + HEIGHT_PER_DEPTH + LABEL_MARGIN + LINE_MARGIN,
                )
                p2 = (node.x + TEXT_MARGIN[0], node.y)
                p3 = (node.x + node.width - TEXT_MARGIN[0], node.y)
                d.polygon((p1, p2, p3), outline=LINE_COLOUR, width=LINE_WIDTH)
                continue

            d.line(
                (
                    (
                        node.x + node.width // 2,
                        node.y
                        - (LABEL_MARGIN if node.is_label else -LABEL_MARGIN)
                        - LINE_MARGIN,
                    ),
                    (
                        parent.x + parent.width // 2,
                        parent.y + HEIGHT_PER_DEPTH + LABEL_MARGIN + LINE_MARGIN,
                    ),
                ),
                LINE_COLOUR,
                LINE_WIDTH,
            )

out.show()

if args.path:
    out.save(args.path)

print("Done!")
