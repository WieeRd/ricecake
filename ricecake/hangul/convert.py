"""Conversion between Hangul Jamo and Hangul Compatibility Jamo."""

# from .offset import *

__all__ = [
    "jamo_to_compat_jamo",
    "compat_jaum_to_choseong",
    "compat_moum_to_jungseong",
    "compat_jaum_to_jongseong",
]


# FIX: all *modern* Jamo can be mapped to Compat Jamo
def jamo_to_compat_jamo(c: str, /) -> str | None:
    """Converts a Hangul Jamo character to a Compatibility Jamo character.

    Returns `None` if there is no corresponding Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a Hangul Jamo.
    """
    raise NotImplementedError


def compat_jaum_to_choseong(c: str, /) -> str | None:
    """Converts a Hangul Compatibility Jaum character to a Jamo Choseong character.

    Returns `None` if there is no corresponding Jamo Choseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    raise NotImplementedError


def compat_moum_to_jungseong(c: str, /) -> str:
    """Converts a Hangul Compatibility Moum character to a Jamo Jungseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Moum.
    """
    raise NotImplementedError


def compat_jaum_to_jongseong(c: str, /) -> str:
    """Converts a Hangul Compatibility Jaum character to a Jamo Jongseong character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo Jaum.
    """
    raise NotImplementedError
