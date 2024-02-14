"""Conversion between Hangul Jamo and Hangul Compatibility Jamo."""

from contextlib import suppress

from . import offset
from ._lookup import (
    CHOSEONG_TO_COMPAT_JAUM,
    COMPAT_JAUM_TO_CHOSEONG,
    COMPAT_JAUM_TO_JONGSEONG,
    JONGSEONG_TO_COMPAT_JAUM,
)

__all__ = [
    "modern_jamo_to_compat_jamo",
    "compat_jaum_to_choseong",
    "compat_moum_to_jungseong",
    "compat_jaum_to_jongseong",
]


# FIX: LATER: refactor repetitive try-except blocks
# | - [ ] return `T | None` instead of raising `ValueError`
# | - [ ] add `classify_jamo() -> tuple[JamoKind, int]`
# | - [ ] `jamo_to_compat_jamo() -> str | None`
# | - [x] RIIR & PyO3
def modern_jamo_to_compat_jamo(c: str, /) -> str:
    """Converts a Hangul Jamo character to a Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a Hangul Jamo.
    """
    with suppress(ValueError):
        i = offset.modern_choseong_offset(c)
        return CHOSEONG_TO_COMPAT_JAUM[i]

    with suppress(ValueError):
        i = offset.modern_jungseong_offset(c)
        return chr(i + offset.MODERN_COMPAT_MOUM_BASE)

    with suppress(ValueError):
        i = offset.modern_jongseong_offset(c)
        return JONGSEONG_TO_COMPAT_JAUM[i - 1]

    raise ValueError("expected a modern Hangul Jamo character")


def compat_jaum_to_choseong(c: str, /) -> str | None:
    """Converts a Hangul Compatibility Jaum character to a Jamo Choseong character.

    Returns `None` if there is no corresponding Jamo Choseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = offset.modern_compat_jaum_offset(c)
    return COMPAT_JAUM_TO_CHOSEONG[i]


def compat_moum_to_jungseong(c: str, /) -> str:
    """Converts a Hangul Compatibility Moum character to a Jamo Jungseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Moum.
    """
    i = offset.modern_compat_moum_offset(c)
    return chr(i + offset.MODERN_JUNGSEONG_BASE)


def compat_jaum_to_jongseong(c: str, /) -> str:
    """Converts a Hangul Compatibility Jaum character to a Jamo Jongseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = offset.modern_compat_jaum_offset(c)
    return COMPAT_JAUM_TO_JONGSEONG[i]
