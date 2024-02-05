"""Conversion between Hangul Jamo and Compatibility Jamo."""


def jamo_to_compat_jamo(c: str, /) -> str | None:
    """Maps a Jamo character to a Compatibility Jamo character."""
    ...


def compat_jaum_to_choseong(c: str, /) -> str | None:
    """Maps a Compatibility Jaum character to a Jamo Choseong character."""
    ...


def compat_moum_to_jungseong(c: str, /) -> str:
    """Maps a Compatibility Moum character to a Jamo Jungseong character."""
    ...


def compat_jaum_to_jongseong(c: str, /) -> str:
    """Maps a Compatibility Jaum character to a Jamo Jongseong character."""
    ...
