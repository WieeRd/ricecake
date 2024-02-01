"""Jamo <-> Compatibility Jamo conversions."""

import unicodedata as ud
from collections.abc import Callable
from typing import TypeVar


def jamo_to_compat_jamo(jamo: str, /) -> str | None:
    """Maps a Jamo character to a Compatibility Jamo character."""
    name = ud.name(jamo).split(" ")[-1]  # HANGUL CHOSEONG "KIYEOK"
    try:
        return ud.lookup(f"HANGUL LETTER {name}")
    except KeyError:
        return None


def compat_jaum_to_choseong(compat_jaum: str, /) -> str | None:
    """Maps a Compatibility Jaum character to a Jamo Choseong character."""
    name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
    try:
        return ud.lookup(f"HANGUL CHOSEONG {name}")
    except KeyError:
        return None


def compat_moum_to_jungseong(compat_moum: str, /) -> str:
    """Maps a Compatibility Moum character to a Jamo Jungseong character."""
    name = ud.name(compat_moum).split(" ")[-1]  # HANGUL LETTER "A"
    return ud.lookup(f"HANGUL JUNGSEONG {name}")


def compat_jaum_to_jongseong(compat_jaum: str, /) -> str:
    """Maps a Compatibility Jaum character to a Jamo Jongseong character."""
    name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
    return ud.lookup(f"HANGUL JONGSEONG {name}")


def decompose_jongseong(jongseong: str, /) -> tuple[str, str] | None:
    """Decomposes a composite Jongseong into tuple of 2 Jongseongs."""
    name = ud.name(jongseong).split(" ")[-1]  # HANGUL JONGSEONG "KIYEOK"

    # SSANG{jaum} e.g. SSANGKIYEOK
    if name.startswith("SSANG"):
        single = name.removeprefix("SSANG")
        char = ud.lookup(f"HANGUL JONGSEONG {single}")
        return char, char

    # {jaum}-{jaum} e.g. RIEUL-KIYEOK
    if "-" in name:
        # NOTE: some archaic Jongseongs such as "ᇄ" are triplets, causing ValueError
        # | but I am no linguist and decided that I do not care about archaic letters
        first, second = name.split("-")
        char1 = ud.lookup(f"HANGUL JONGSEONG {first}")
        char2 = ud.lookup(f"HANGUL JONGSEONG {second}")
        return char1, char2

    return None


# FEAT: compat jaum to choseong pattern ("ㄱ" -> "[ㄱ가-깋]")

if __name__ == "__main__":
    import ricecake.hangul as hg

    T = TypeVar("T")
    def _create_lookup_table(
        convert: Callable[[str], T], base: int, end: int
    ) -> list[T]:
        return [convert(chr(code)) for code in range(base, end + 1)]

    JAMO_TO_COMPAT_JAMO = _create_lookup_table(
        jamo_to_compat_jamo,
        hg.JAMO_BASE,
        hg.JAMO_END,
    )
    COMPAT_JAUM_TO_CHOSEONG = _create_lookup_table(
        compat_jaum_to_choseong,
        hg.COMPAT_MODERN_JAUM_BASE,
        hg.COMPAT_MODERN_JAUM_END,
    )
    COMPAT_MOUM_TO_JUNGSEONG = _create_lookup_table(
        compat_moum_to_jungseong,
        hg.COMPAT_MODERN_MOUM_BASE,
        hg.COMPAT_MODERN_MOUM_END,
    )
    COMPAT_JAUM_TO_JONGSEONG = _create_lookup_table(
        compat_jaum_to_jongseong,
        hg.COMPAT_MODERN_JAUM_BASE,
        hg.COMPAT_MODERN_JAUM_END,
    )
    DECOMPOSE_JONGSEONG = _create_lookup_table(
        decompose_jongseong,
        hg.MODERN_JONGSEONG_BASE,
        hg.MODERN_JONGSEONG_END,
    )

    print(f"JAMO_TO_COMPAT_JAMO = {JAMO_TO_COMPAT_JAMO}\n")
    print(f"COMPAT_JAUM_TO_CHOSEONG = {COMPAT_JAUM_TO_CHOSEONG}\n")
    print(f"COMPAT_MOUM_TO_JUNGSEONG = {COMPAT_MOUM_TO_JUNGSEONG}\n")
    print(f"COMPAT_JAUM_TO_JONGSEONG = {COMPAT_JAUM_TO_JONGSEONG}\n")
    print(f"DECOMPOSE_JONGSEONG = {DECOMPOSE_JONGSEONG}\n")
