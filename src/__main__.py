from PIL import Image, ImageDraw

from src.config import *
from src.parser_ import Parser

parser = Parser(input("Type in the sentence: "))
node = parser.get_head()
ends, width, height = node.get_size_and_ends(FONT)
out = Image.new("RGB", (width, height), BG_COLOUR)
d = ImageDraw.Draw(out)
x = CONTAINER_MARGIN

for node, line in ends:
    node.set_size(
        x,
        (line - 1) * HEIGHT_PER_DEPTH + (line - 1) * TEXT_MARGIN[1] + CONTAINER_MARGIN,
    )
    d.text(
        (node.x, node.y),
        node.text,
        fill=END_COLOUR,
        font=FONT,
    )
    x += node.width + TEXT_MARGIN[0]

    while node := node.head:
        if not all([i.x is not None for i in node.children]):
            # children's pos aren't set yet, revisit the node later
            continue
        rnode = max(node.children, key=lambda x: x.x)
        lnode = min(node.children, key=lambda x: x.x)
        node.set_size(
            lnode.x + (rnode.x + rnode.width - lnode.x) // 2 - node.width // 2,
            node.children[0].y - HEIGHT_PER_DEPTH - TEXT_MARGIN[1],
        )
        d.text(
            (node.x, node.y),
            node.text,
            fill=LABEL_COLOUR,
            font=FONT,
        )
        for child in node.children:
            if node.draws_triangle:
                p1 = (node.x + node.width // 2, node.y + HEIGHT_PER_DEPTH)
                p2 = (child.x + TEXT_MARGIN[0], child.y)
                p3 = (child.x + child.width - TEXT_MARGIN[0], child.y)
                d.polygon((p1, p2, p3), outline=LINE_COLOUR, width=LINE_WIDTH)
                continue
            d.line(
                (
                    (node.x + node.width // 2, node.y + HEIGHT_PER_DEPTH),
                    (child.x + child.width // 2, child.y),
                ),
                LINE_COLOUR,
                LINE_WIDTH,
            )

# TODO: File output CLI argument
out.show()
