import typing as t

from src.config import *


class Node:
    def __init__(self, head: t.Optional["Node"] = None) -> None:
        self.head = head
        if head:
            head.children.append(self)
        self.children: list[Node] = []
        self._text: str = ""
        self.width = 0
        self._x = 0
        self.y = 0
        self.draws_triangle = False
        self.depth = 1

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, val: int) -> None:
        delta = val - self._x
        self._x = val
        for child in self.children:
            child.x += delta

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        if val and val[0] == "^":
            val = val[1:]
            self.draws_triangle = True
        self._text = val
        self.width = int(FONT.getlength(val))

    def __repr__(self) -> str:
        return f"<Node text={self.text!r}>"

    @property
    def children_length(self) -> int:
        return sum(i.width for i in self.children) + (
            TEXT_MARGIN[0] + (LABEL_MARGIN * 2) * self.is_label
        ) * (len(self.children) - 1)

    @property
    def is_label(self) -> bool:
        return not self.is_end

    @property
    def is_end(self) -> bool:
        return not self.children

    def calculate_and_get_nodes(self):
        depths = [[self]]
        current = depths[0]
        offset = 0
        while current:
            temp = []
            for head in current:
                temp.extend(head.children)
                x = head.x + head.width // 2 - head.children_length // 2
                offset = min(x, offset)
                for child in head.children:
                    if child.is_label:
                        x += LABEL_MARGIN
                    child.depth = head.depth + 1
                    child.x = x
                    child.y = (
                        HEIGHT_PER_DEPTH + TEXT_MARGIN[1] + LABEL_MARGIN * 2
                    ) * len(depths) + CONTAINER_MARGIN
                    x += child.width + TEXT_MARGIN[0] + LABEL_MARGIN * self.is_label

            if temp:
                depths.append(temp)
            current = temp

        self.x += CONTAINER_MARGIN - offset
        self.y = CONTAINER_MARGIN
        canvas_width = 0

        def check_overlap(depths, i, recurse=True):
            nonlocal canvas_width
            before = None
            for node in depths[i]:
                if (
                    before
                    and (
                        offset := node.x
                        - (
                            before.x
                            + before.width
                            + TEXT_MARGIN[0]
                            + LABEL_MARGIN * (before.is_label + node.is_label)
                        )
                    )
                    < 0
                ):
                    node.head.x -= offset
                    if recurse:
                        check_overlap(depths, i - 1, True)

                before = node
                canvas_width = max(
                    node.x + node.width + LABEL_MARGIN * node.is_label, canvas_width
                )

                # center all the head "recursively"
                head = node.head
                while head:
                    rnode = max(head.children, key=lambda x: x.x)
                    lnode = min(head.children, key=lambda x: x.x)
                    head._x = (
                        lnode.x
                        + (rnode.x + rnode.width - lnode.x) // 2
                        - head.width // 2
                    )
                    if recurse:
                        check_overlap(
                            depths, head.depth - 1, False  # don't recurse here
                        )
                    head = head.head

        for i in range(len(depths)):
            check_overlap(depths, i)

        canvas_height = (
            HEIGHT_PER_DEPTH * len(depths)
            + (len(depths) - 1) * (TEXT_MARGIN[1] + LABEL_MARGIN * 2)
            + CONTAINER_MARGIN * 2
        )
        return depths, (canvas_width + CONTAINER_MARGIN, canvas_height)

    def set_size(self, x, y):
        self.x = x
        self.y = y
