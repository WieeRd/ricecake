"""(De)composition of Hangul Jamo and Syllable."""

from . import offset as o

__all__ = ["compose", "decompose"]


# FEAT: LATER: compose syllable compat jamo
# | - provide separate function
# | - boolean flag parameter
# | - normalize the input every time
def compose(cho: str, jung: str, jong: str | None) -> str:
    """Composes Choseong, Jungseong, and an optional Jongseong into a Syllable.

    Raises:
        ValueError: If the characters are not appropriate Hangul Jamos.
    """
    return chr(
        o.modern_choseong_offset(cho) * o.CHOSEONG_COEF
        + o.modern_jongseong_offset(jung) * o.JUNGSEONG_COEF
        + (o.modern_jongseong_offset(jong) if jong else 0)
        + o.SYLLABLE_BASE
    )


def decompose(c: str, /) -> tuple[str, str, str | None]:
    """Decomposes a Syllable into Choseong, Jungseong, and an optional Jongseong.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    syl = o.syllable_offset(c)

    cho = syl // o.CHOSEONG_COEF
    jung = syl % (o.CHOSEONG_COEF) // o.JUNGSEONG_COEF
    jong = syl % o.JUNGSEONG_COEF

    return (
        chr(cho + o.MODERN_CHOSEONG_BASE),
        chr(jung + o.MODERN_JUNGSEONG_BASE),
        chr(jong + o.MODERN_JONGSEONG_BASE - 1) if jong else None,
    )


# FEAT: decompose composite Jaum and Moum into tuple of str
# |
# | - [ ] There are 5 cases, cho/jung/jong and compat jaum/moum.
# |   Which should be included and which should be not?
# |
# | - [ ] Should it be keyboard-based or shape-based?
# |   "ㅐ" is "ㅏ" + "ㅣ" but it can be typed at once with a keyboard.
# |   If so, should "ㅙ" be decomposed to ("ㅗ", "ㅐ") or ("ㅗ", "ㅏ", "ㅣ")?
