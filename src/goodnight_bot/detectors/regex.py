import re

from goodnight_bot.detectors.base import DetectorStrategy

_PATTERNS = [
    r"споко[йь]н(?!о(?!й))",
    r"спок[аоиы]?[йь]н(?!о(?!й))",
    r"споки(?!льно)",
    r"спок\s*ноч",
    r"спокн[аоиы]?[йь]",
    r"баиньки",
]

_COMBINED = re.compile(
    r"(?i)(?:"
    + r"|".join(_PATTERNS)
    + r")",
)


class RegexDetector(DetectorStrategy):
    def is_goodnight(self, text: str) -> bool:
        if not text:
            return False
        return bool(_COMBINED.search(text))