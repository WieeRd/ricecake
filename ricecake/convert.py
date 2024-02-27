"""Conversion between Hangul Jamo and Hangul Compatibility Jamo."""

from contextlib import suppress

from . import offset as o
from ._lookup import (
    CHOSEONG_TO_COMPAT_JAUM,
    COMPAT_JAUM_TO_CHOSEONG,
    COMPAT_JAUM_TO_JONGSEONG,
    JONGSEONG_TO_COMPAT_JAUM,
)

__all__ = [
    "jamo_to_compat_jamo",
    "compat_jaum_to_choseong",
    "compat_moum_to_jungseong",
    "compat_jaum_to_jongseong",
]


# FIX: LATER: refactor repetitive try-except blocks
# | - [ ] return `T | None` instead of raising `ValueError`
# | - [ ] add `classify_jamo() -> tuple[JamoKind, int]`
# | - [ ] `jamo_to_compat_jamo() -> str | None`
# | - [x] RIIR & PyO3
def jamo_to_compat_jamo(jamo: str) -> str:
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
        return JONGSEONG_TO_COMPAT_JAUM[i - 1]

    raise ValueError("expected a modern Hangul Jamo character")


def compat_jaum_to_choseong(compat_jaum: str) -> str | None:
    """Converts a Hangul Compatibility Jaum character to a Jamo Choseong character.

    Returns `None` if there is no corresponding Jamo Choseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = o.compat_jaum_offset(compat_jaum)
    return COMPAT_JAUM_TO_CHOSEONG[i]


def compat_moum_to_jungseong(compat_moum: str) -> str:
    """Converts a Hangul Compatibility Moum character to a Jamo Jungseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Moum.
    """
    i = o.compat_moum_offset(compat_moum)
    return chr(i + o.MODERN_JUNGSEONG_BASE)


def compat_jaum_to_jongseong(compat_jaum: str) -> str:
    """Converts a Hangul Compatibility Jaum character to a Jamo Jongseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    i = o.compat_jaum_offset(compat_jaum)
    return COMPAT_JAUM_TO_JONGSEONG[i]
