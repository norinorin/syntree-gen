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
                self.cursor -= 1
                if self.depth < 1:
                    self._raise_syntax_error("square brackets don't match")
                if "[" in buffer or "]" in buffer:
                    self._raise_syntax_error("text can't have square brackets")
                return "".join(buffer)
        return ""  # unexpected eof, handled in get_head

    def get_text(self) -> str:
        buffer = []
        while not self.is_eof:
            if self.next().isspace():
                if "[" in buffer or "]" in buffer:
                    self._raise_syntax_error("label can't have square brackets")
                return "".join(buffer)
            buffer.append(self.current)

    def get_head(self) -> Node:
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
                current = current.head
            else:
                child = Node(current)
                child.text = self.consume_this_depth()
            self.next()
        if self.depth > 1:
            self._raise_syntax_error("unexpected eof")
        return current

    def _raise_syntax_error(self, msg):
        raise SyntaxError(
            f"{msg} at {self.cursor}\n"
            f"{self.text[:self.cursor+10]}\n"
            f"{' '*self.cursor}^"
        )
