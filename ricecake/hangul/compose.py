"""(De)composition of Hangul Jamo and Syllable."""


def compose(cho: str, jung: str, jong: str | None) -> str:
    """Composes Choseong, Jungseong, and Jongseong into a Syllable."""
    ...


def decompose(syl: str) -> tuple[str, str, str | None]:
    """Decomposes a Syllable into Choseong, Jungseong, and Jongseong."""
    ...


# FEAT: decompose composite Jaum and Moum into tuple of str
# |
# | - [ ] There are 5 cases, cho/jung/jong and compat jaum/moum.
# |   Which should be included and which should be not?
# |
# | - [ ] Should it be keyboard-based or shape-based?
# |   "ㅐ" is "ㅏ" + "ㅣ" but it can be typed at once with a keyboard.
# |   If so, should "ㅙ" be decomposed to ("ㅗ", "ㅐ") or ("ㅗ", "ㅏ", "ㅣ")?
