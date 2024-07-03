import os

from src.nodes import Node


class Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.cursor = -1
        self.depth = 0

    @property
    def is_eof(self) -> bool:
        return self.cursor >= len(self.text) - 1

    @property
    def current(self) -> str:
        return self.text[self.cursor] if not self.is_eof else ""

    def skip_ws(self) -> None:
        if self.cursor < 0:
            self.cursor = 0
        while self.current.isspace():
            self.next()

    @property
    def length(self) -> int:
        return len(self.text)

    def next(self) -> str:
        if self.is_eof:
            return ""
        self.cursor += 1
        return self.text[self.cursor]

    def consume_this_depth(self) -> str:
        buffer = []
        while not self.is_eof:
            buffer.append(self.current)
            if self.next() in "[]":
                if self.depth < 1:
                    self._raise_syntax_error("square brackets don't match")
                if "[" in buffer or "]" in buffer:
                    self._raise_syntax_error("text can't have square brackets")
                self.cursor -= 1
                return "".join(buffer)
        return ""  # unexpected eof, handled in get_first_parent

    def get_text(self) -> str:
        buffer = []
        while not self.is_eof:
            if self.next().isspace():
                if "[" in buffer or "]" in buffer:
                    self._raise_syntax_error("label can't have square brackets")
                return "".join(buffer)
            if self.current in "[]":
                self._raise_syntax_error("label can't have square brackets")
            buffer.append(self.current)
        return ""

    def get_first_parent(self) -> Node:
        current = None
        while not self.is_eof:
            self.skip_ws()
            char = self.current
            if char == "[":
                self.depth += 1
                current = Node(current)
                current.text = self.get_text()
            elif char == "]":
                self.depth -= 1
                if self.depth < 1:
                    self._raise_syntax_error("square brackets don't match")
                current = current.parent
            else:
                child = Node(current)
                child.text = self.consume_this_depth()
            self.next()
        if self.depth > 1:
            self._raise_syntax_error("unexpected eof")
        if not current:
            self._raise_syntax_error("input invalid")
        return current

    def _raise_syntax_error(self, msg):
        n = os.get_terminal_size().columns - 6
        end = min(self.length - self.cursor, n // 2)
        start = n - end
        ellipsis_start = self.cursor - start > 0
        ellipsis_end = self.cursor + end < self.length
        raise SyntaxError(
            f"{msg} at {self.cursor+1}\n"
            f"{'...' * ellipsis_start}{self.text[self.cursor-start:self.cursor+end]}{'...' * ellipsis_end}\n"
            f"{' '*(min(n-end, self.cursor) + 3 * ellipsis_start)}^"
        )
