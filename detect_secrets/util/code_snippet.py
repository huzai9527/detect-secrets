from typing import Generator
from typing import List

from .color import AnsiColor
from .color import colorize


def get_code_snippet(
    lines: List[str],
    line_number: int,
    lines_of_context: int = 5,
) -> 'CodeSnippet':
    """
    :param lines: an iterator of lines in the file
    :param line_number: line which you want to focus on
    :param lines_of_context: how many lines to display around the line you want
        to focus on.
    """
    target_line_index = line_number - 1
    end_line_index = target_line_index + lines_of_context + 1

    if target_line_index <= lines_of_context:
        start_line_index = 0
    else:
        start_line_index = target_line_index - lines_of_context
        target_line_index = lines_of_context

    return CodeSnippet(
        snippet=lines[start_line_index:end_line_index],
        start_line=start_line_index,
        target_index=target_line_index,
    )


class CodeSnippet:

    def __init__(self, snippet: List[str], start_line: int, target_index: int) -> None:
        """
        :param snippet: lines of code extracted from file
        :param start_line: first line number in segment
        :param target_index: index in snippet of target line
        """
        self.lines = snippet
        self.start_line = start_line
        self.target_index = target_index

    @property
    def target_line(self) -> str:
        return self.lines[self.target_index]

    @target_line.setter
    def target_line(self, value: str) -> None:
        self.lines[self.target_index] = value

    @property
    def previous_line(self) -> str:
        if self.target_index == 0 or len(self.lines) < self.target_index:
            return ''
        return self.lines[self.target_index - 1]

    def add_line_numbers(self) -> 'CodeSnippet':
        for index, line in enumerate(self.lines):
            self.lines[index] = u'{}:{}'.format(
                self.get_line_number(self.start_line + index + 1),
                line,
            )

        return self

    def highlight_line(self, payload: str) -> 'CodeSnippet':
        """
        :param payload: string to highlight, on chosen line
        """
        index_of_payload = self.target_line.lower().index(payload.lower())
        end_of_payload = index_of_payload + len(payload)

        self.target_line = u'{}{}{}'.format(
            self.target_line[:index_of_payload],
            self.apply_highlight(self.target_line[index_of_payload:end_of_payload]),
            self.target_line[end_of_payload:],
        )

        return self

    def get_line_number(self, line_number: int) -> str:
        """Broken out, for custom colorization."""
        return colorize(str(line_number), AnsiColor.LIGHT_GREEN)

    def apply_highlight(self, payload: str) -> str:
        """Broken out, for custom colorization."""
        return colorize(payload, AnsiColor.RED_BACKGROUND)

    def __str__(self) -> str:
        return '\n'.join(self.lines)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.lines
