from src.config import *


def draw_nodes(nodes, draw):
    for siblings in nodes:
        for node in siblings:
            if node.is_label:
                draw.rounded_rectangle(
                    (
                        (node.x - LABEL_MARGIN, node.y - LABEL_MARGIN),
                        (
                            node.x + node.width + LABEL_MARGIN,
                            node.y + HEIGHT_PER_DEPTH + LABEL_MARGIN,
                        ),
                    ),
                    radius=RECTANGLE_RADIUS,
                    fill=get_label_colour(node.text)[0],
                )
            draw.text(
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
                    draw.polygon((p1, p2, p3), outline=LINE_COLOUR, width=LINE_WIDTH)
                    continue

                draw.line(
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
