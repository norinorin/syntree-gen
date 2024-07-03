import os

from src.nodes import Node

ESCAPE_SEQUENCES = {"\\0": "\u2205", "\\s": " ", "\\lb": "[", "\\rb": "]"}


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

    def _join_buffer(self, buffer) -> str:
        ret = "".join(buffer)
        for old, new in ESCAPE_SEQUENCES.items():
            ret = ret.replace(old, new)
        return ret

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
                return self._join_buffer(buffer)
        return ""  # unexpected eof, handled in get_first_parent

    def get_text(self) -> str:
        buffer = []
        while not self.is_eof:
            if self.next().isspace():
                if "[" in buffer or "]" in buffer:
                    self._raise_syntax_error("label can't have square brackets")
                return self._join_buffer(buffer)
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
        lhcc = min(self.cursor, n // 2)  # left hand char count
        start = self.cursor - lhcc
        end = self.cursor + (n - lhcc)
        ellipsis_start = start > 0
        ellipsis_end = end < self.length
        raise SyntaxError(
            f"{msg} at {self.cursor+1}\n"
            f"{'...' * ellipsis_start}{self.text[start:end]}{'...' * ellipsis_end}\n"
            f"{' '*((self.cursor - start) + 3 * ellipsis_start)}^"
        )
