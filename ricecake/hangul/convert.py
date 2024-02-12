"""Conversion between Hangul Jamo and Compatibility Jamo."""

from .offset import MODERN_JUNGSEONG_BASE, modern_compat_moum_offset

__all__ = [
    "jamo_to_compat_jamo",
    "compat_jaum_to_choseong",
    "compat_moum_to_jungseong",
    "compat_jaum_to_jongseong",
]


def jamo_to_compat_jamo(c: str, /) -> str | None:
    """Converts a Jamo character to a Compatibility Jamo character."""
    raise NotImplementedError


def compat_jaum_to_choseong(c: str, /) -> str | None:
    """Converts a Compatibility Jaum character to a Jamo Choseong character."""
    raise NotImplementedError


def compat_moum_to_jungseong(c: str, /) -> str:
    """Converts a Compatibility Moum character to a Jamo Jungseong character."""
    offset = modern_compat_moum_offset(c)
    return chr(offset + MODERN_JUNGSEONG_BASE)


def compat_jaum_to_jongseong(c: str, /) -> str:
    """Converts a Compatibility Jaum character to a Jamo Jongseong character."""
    raise NotImplementedError
