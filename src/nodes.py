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
        self.x = None
        self.y = None
        self.draws_triangle = False

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        if val[0] == "^":
            val = val[1:]
            self.draws_triangle = True
        self._text = val
        self.width = int(FONT.getlength(val))

    def __repr__(self) -> str:
        return f"<Node text={self.text!r}>"

    def _get_ends(self, font, child=None, depth=1):
        ret = []
        node = child or self
        if not node.children:
            return [(node, depth)]

        for child in node.children:
            ret.extend(self._get_ends(font, child, depth + 1))

        return ret

    def get_size_and_ends(self, font):
        ends = self._get_ends(font)
        depth = max(ends, key=lambda x: x[1])[1]
        height = (
            HEIGHT_PER_DEPTH * depth
            + (depth - 1) * TEXT_MARGIN[1]
            + CONTAINER_MARGIN * 2
        )
        width = (
            sum([i[0].width for i in ends])
            + (len(ends) - 1) * TEXT_MARGIN[0]
            + CONTAINER_MARGIN * 2
        )
        return ends, width, height

    def set_size(self, x, y, overwrite=False):
        if self.x is not None and self.y is not None and not overwrite:
            return

        self.x = x
        self.y = y
