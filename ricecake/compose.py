"""(De)composition of Hangul Jamo and Syllable."""

from . import offset as o

__all__ = [
    "compose",
    "decompose",
    "get_choseong",
    "get_jungseong",
    "get_jongseong",
    "set_choseong",
    "set_jungseong",
    "set_jongseong",
    "decompose_jongseong",
]


DECOMPOSE_JONGSEONG = [
    ("ᆨ", None),
    ("ᆨ", "ᆨ"),
    ("ᆨ", "ᆺ"),
    ("ᆫ", None),
    ("ᆫ", "ᆽ"),
    ("ᆫ", "ᇂ"),
    ("ᆮ", None),
    ("ᆯ", None),
    ("ᆯ", "ᆨ"),
    ("ᆯ", "ᆷ"),
    ("ᆯ", "ᆸ"),
    ("ᆯ", "ᆺ"),
    ("ᆯ", "ᇀ"),
    ("ᆯ", "ᇁ"),
    ("ᆯ", "ᇂ"),
    ("ᆷ", None),
    ("ᆸ", None),
    ("ᆸ", "ᆺ"),
    ("ᆺ", None),
    ("ᆺ", "ᆺ"),
    ("ᆼ", None),
    ("ᆽ", None),
    ("ᆾ", None),
    ("ᆿ", None),
    ("ᇀ", None),
    ("ᇁ", None),
    ("ᇂ", None),
]


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
        o.choseong_offset(cho) * o.CHOSEONG_COEF
        + o.jungseong_offset(jung) * o.JUNGSEONG_COEF
        + (o.jongseong_offset(jong) if jong else 0)
        + o.SYLLABLE_BASE
    )


def decompose(syllable: str) -> tuple[str, str, str | None]:
    """Decomposes a Syllable into Choseong, Jungseong, and an optional Jongseong.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    syl = o.syllable_offset(syllable)

    cho = syl // o.CHOSEONG_COEF
    jung = syl % o.CHOSEONG_COEF // o.JUNGSEONG_COEF
    jong = syl % o.JUNGSEONG_COEF

    return (
        chr(cho + o.MODERN_CHOSEONG_BASE),
        chr(jung + o.MODERN_JUNGSEONG_BASE),
        chr(jong + o.MODERN_JONGSEONG_BASE - 1) if jong else None,
    )


def get_choseong(syllable: str) -> str:
    """Extracts Choseong from a Syllable.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    cho = o.syllable_offset(syllable) // o.CHOSEONG_COEF
    return chr(cho + o.MODERN_CHOSEONG_BASE)


def get_jungseong(syllable: str) -> str:
    """Extracts Jungseong from a Syllable.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    jung = o.syllable_offset(syllable) % o.CHOSEONG_COEF // o.JUNGSEONG_COEF
    return chr(jung + o.MODERN_JUNGSEONG_BASE)


def get_jongseong(syllable: str) -> str | None:
    """Extracts Jongseong from a Syllable, if there is one.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    jong = o.syllable_offset(syllable) % o.JUNGSEONG_COEF
    return chr(jong + o.MODERN_JONGSEONG_BASE - 1) if jong else None


def set_choseong(syllable: str, choseong: str) -> str:
    """Replaces the Choseong of the given Syllable.

    Raises:
        ValueError:
            - If `syllable` is not a Hangul Syllable.
            - If `choseong` is not a Hangul Jamo Choseong.
    """
    syl = o.syllable_offset(syllable)
    cho = o.choseong_offset(choseong)
    return chr(cho * o.CHOSEONG_COEF + syl % o.CHOSEONG_COEF + o.SYLLABLE_BASE)


def set_jungseong(syllable: str, jungseong: str) -> str:
    """Replaces the Jungseong of the given Syllable.

    Raises:
        ValueError:
            - If `syllable` is not a Hangul Syllable.
            - If `jungseong` is not a Hangul Jamo Jungseong.
    """
    syl = o.syllable_offset(syllable)
    new_jung = o.jungseong_offset(jungseong)
    old_jung = syl % o.CHOSEONG_COEF // o.JUNGSEONG_COEF
    return chr(syl + (new_jung - old_jung) * o.JUNGSEONG_COEF + o.SYLLABLE_BASE)


def set_jongseong(syllable: str, jongseong: str | None) -> str:
    """Replaces the Jongseong of the given Syllable.

    Raises:
        ValueError:
            - If `syllable` is not a Hangul Syllable.
            - If `jongseong` is not a Hangul Jamo Jongseong.
    """
    syl = o.syllable_offset(syllable)
    jong = o.jongseong_offset(jongseong) if jongseong else 0
    return chr(syl - syl % o.JONGSEONG_COUNT + jong + o.SYLLABLE_BASE)


def decompose_jongseong(jongseong: str) -> tuple[str, str | None]:
    """Decomposes a composite Jongseong into tuple of 2 Jongseong characters.

    Non-composite Jongseongs are returned as `(itself, None)`.

    Raises:
        ValueError: If the character is not a Hangul Jamo Jongseong.
    """
    return DECOMPOSE_JONGSEONG[o.jongseong_offset(jongseong) - 1]


# FEAT: decompose composite Jaum and Moum into tuple of str
# |
# | - [ ] There are 5 cases, cho/jung/jong and compat jaum/moum.
# |   Which should be included and which should be not?
# |
# | - [ ] Should it be keyboard-based or shape-based?
# |   "ㅐ" is "ㅏ" + "ㅣ" but it can be typed at once with a keyboard.
# |   If so, should "ㅙ" be decomposed to ("ㅗ", "ㅐ") or ("ㅗ", "ㅏ", "ㅣ")?
