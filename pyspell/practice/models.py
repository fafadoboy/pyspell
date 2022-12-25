from dataclasses import dataclass
from typing import Any

WORD_ROW_NAME_LOC = 0
WORD_ROW_DESCRIPTION_LOC = 1
WORD_ROW_AUDIO_LOC = 2

@dataclass
class Word:
    word: Any
    answer: str