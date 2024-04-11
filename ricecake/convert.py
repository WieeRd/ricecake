"""Conversion between Hangul Jamo and Hangul Compatibility Jamo."""

from contextlib import suppress

from . import offset as o

__all__ = [
    "to_compat_jamo",
    "to_choseong",
    "to_jungseong",
    "to_jongseong",
]


CHOSEONG_TO_COMPAT_JAUM = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JONGSEONG_TO_COMPAT_JAUM = [
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

COMPAT_JAUM_TO_CHOSEONG = [
    "ᄀ",
    "ᄁ",
    None,
    "ᄂ",
    "ᅜ",
    "ᅝ",
    "ᄃ",
    "ᄄ",
    "ᄅ",
    "ꥤ",
    "ꥨ",
    "ꥩ",
    "ꥬ",
    None,
    None,
    "ᄚ",
    "ᄆ",
    "ᄇ",
    "ᄈ",
    "ᄡ",
    "ᄉ",
    "ᄊ",
    "ᄋ",
    "ᄌ",
    "ᄍ",
    "ᄎ",
    "ᄏ",
    "ᄐ",
    "ᄑ",
    "ᄒ",
]

COMPAT_JAUM_TO_JONGSEONG = [
    "ᆨ",
    "ᆩ",
    "ᆪ",
    "ᆫ",
    "ᆬ",
    "ᆭ",
    "ᆮ",
    "ퟍ",
    "ᆯ",
    "ᆰ",
    "ᆱ",
    "ᆲ",
    "ᆳ",
    "ᆴ",
    "ᆵ",
    "ᆶ",
    "ᆷ",
    "ᆸ",
    "ퟦ",
    "ᆹ",
    "ᆺ",
    "ᆻ",
    "ᆼ",
    "ᆽ",
    "ퟹ",
    "ᆾ",
    "ᆿ",
    "ᇀ",
    "ᇁ",
    "ᇂ",
]


# FIX: LATER: refactor repetitive try-except blocks
# | - [ ] return `T | None` instead of raising `ValueError`
# | - [ ] add `classify_jamo() -> tuple[JamoKind, int]`
# | - [ ] `jamo_to_compat_jamo() -> str | None`
# | - [x] RIIR & PyO3
def to_compat_jamo(jamo: str) -> str:
    """Converts a Hangul Jamo character to a Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a Hangul Jamo.
    """
    with suppress(ValueError):
        i = o.choseong_offset(jamo)
        return CHOSEONG_TO_COMPAT_JAUM[i]

    with suppress(ValueError):
        i = o.jungseong_offset(jamo)
        return chr(i + o.MODERN_COMPAT_MOUM_BASE)

    with suppress(ValueError):
        i = o.jongseong_offset(jamo)
        return JONGSEONG_TO_COMPAT_JAUM[i]

    raise ValueError("expected a modern Hangul Jamo character")


def to_choseong(compat_jaum: str) -> str | None:
    """Converts a Hangul Compatibility Jaum character to a Jamo Choseong character.

    Returns `None` if there is no corresponding Jamo Choseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = o.compat_jaum_offset(compat_jaum)
    return COMPAT_JAUM_TO_CHOSEONG[i]


def to_jungseong(compat_moum: str) -> str:
    """Converts a Hangul Compatibility Moum character to a Jamo Jungseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Moum.
    """
    i = o.compat_moum_offset(compat_moum)
    return chr(i + o.MODERN_JUNGSEONG_BASE)


def to_jongseong(compat_jaum: str) -> str:
    """Converts a Hangul Compatibility Jaum character to a Jamo Jongseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = o.compat_jaum_offset(compat_jaum)
    return COMPAT_JAUM_TO_JONGSEONG[i]
