"""(De)composition of Hangul Jamo and Syllable."""

from . import offset

__all__ = ["compose", "decompose"]

# FEAT: `*_END - *_START + 1` -> `*_COUNT` -> `*_COEF`
CHOSEONG_COEF = 21 * 28
JUNGSEONG_COEF = 28
JONGSEONG_COEF = 1


def compose(cho: str, jung: str, jong: str | None) -> str:
    """Composes Choseong, Jungseong, and an optional Jongseong into a Syllable.

    Raises:
        ValueError: If the characters are not appropriate Hangul Jamos.
    """
    return chr(
        offset.modern_choseong_offset(cho) * CHOSEONG_COEF
        + offset.modern_jongseong_offset(jung) * JUNGSEONG_COEF
        + (offset.modern_jongseong_offset(jong) if jong else 0)
        + offset.SYLLABLE_BASE
    )


def decompose(syl: str) -> tuple[str, str, str | None]:
    """Decomposes a Syllable into Choseong, Jungseong, and Jongseong."""
    raise NotImplementedError


# FEAT: decompose composite Jaum and Moum into tuple of str
# |
# | - [ ] There are 5 cases, cho/jung/jong and compat jaum/moum.
# |   Which should be included and which should be not?
# |
# | - [ ] Should it be keyboard-based or shape-based?
# |   "ㅐ" is "ㅏ" + "ㅣ" but it can be typed at once with a keyboard.
# |   If so, should "ㅙ" be decomposed to ("ㅗ", "ㅐ") or ("ㅗ", "ㅏ", "ㅣ")?
