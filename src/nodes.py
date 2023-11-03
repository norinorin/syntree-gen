import typing as t

from src.config import *


class Node:
    def __init__(self, head: t.Optional["Node"] = None) -> None:
        self.head = head
        if head:
            head.children.append(self)
        self.children: list[Node] = []
        self._text: str = ""
        # this only accounts for the text, excluding margins and containers
        self.width = 0
        # set this var directly unless you want to also shift the children's pos accordingly
        self._x = 0
        self.y = 0
        self.draws_triangle = False
        # optimisations
        self.depth = 1
        self.index = 0

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
        return (
            sum(i.width for i in self.children)
            + (TEXT_MARGIN[0]) * (len(self.children) - 1)
            + sum([LABEL_MARGIN * 2 for i in self.children if i.is_label])
        )

    @property
    def is_label(self) -> bool:
        return not self.is_end

    @property
    def is_end(self) -> bool:
        return not self.children

    @staticmethod
    def check_overlap(depths, i, skip=0):
        before = None
        iter_ = iter(depths[i])
        for _ in range(skip):
            next(iter_)
        for node in iter_:
            if (
                before
                and (
                    offset := (
                        before.x
                        + before.width
                        + TEXT_MARGIN[0]
                        + LABEL_MARGIN * (before.is_label + node.is_label)
                    )
                    - node.x
                )
                > 0
            ):
                node.x += offset

                # center all the heads recursively
                head = node.head
                while head:
                    rnode = max(head.children, key=lambda x: x.x)
                    lnode = min(head.children, key=lambda x: x.x)
                    head._x = (
                        lnode.x
                        + (rnode.x + rnode.width - lnode.x) // 2
                        - head.width // 2
                    )
                    # head is shifted now, may overlap so check for that
                    Node.check_overlap(depths, head.depth - 1, head.index + 1)
                    head = head.head

            before = node

    def calculate_and_get_nodes(self):
        depths = [[self]]
        current = depths[0]
        while current:
            temp = []
            for head in current:
                temp.extend(head.children)
                x = head.x + head.width // 2 - head.children_length // 2
                for i, child in enumerate(head.children):
                    if child.is_label:
                        x += LABEL_MARGIN
                    child.depth = head.depth + 1
                    child.index = i
                    child.x = x
                    child.y = (
                        HEIGHT_PER_DEPTH + TEXT_MARGIN[1] + LABEL_MARGIN * 2
                    ) * len(depths) + CONTAINER_MARGIN
                    x += child.width + TEXT_MARGIN[0] + LABEL_MARGIN * self.is_label

            if temp:
                depths.append(temp)
            current = temp

        self.y = CONTAINER_MARGIN
        # naturally, some portion of the diagram will be out of frame
        # shift it to the right
        self.x -= min([j.x for i in depths for j in i]) - CONTAINER_MARGIN

        for i in range(len(depths)):
            Node.check_overlap(depths, i)

        canvas_height = (
            HEIGHT_PER_DEPTH * len(depths)
            + (len(depths) - 1) * (TEXT_MARGIN[1] + LABEL_MARGIN * 2)
            + CONTAINER_MARGIN * 2
        )
        canvas_width = (
            max([j.x + j.width for i in depths for j in i]) + CONTAINER_MARGIN
        )
        return depths, (canvas_width, canvas_height)
