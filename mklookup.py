#!/usr/bin/env python

"""Generates various lookup tables with the help of `unicodedata` module.

- Conversions between Jamo and Compatibility Jamo.
- Decomposing composite Jaums and Moums.
"""

import unicodedata as ud
from collections.abc import Callable
from typing import TypeVar


def jamo_to_compat_jamo(jamo: str) -> str | None:
    name = ud.name(jamo).split(" ")[-1]  # HANGUL CHOSEONG "KIYEOK"
    try:
        return ud.lookup(f"HANGUL LETTER {name}")
    except KeyError:
        return None


def compat_jaum_to_choseong(compat_jaum: str) -> str | None:
    name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
    try:
        return ud.lookup(f"HANGUL CHOSEONG {name}")
    except KeyError:
        return None


def compat_jaum_to_jongseong(compat_jaum: str) -> str:
    name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
    return ud.lookup(f"HANGUL JONGSEONG {name}")


def decompose_jongseong(jongseong: str) -> tuple[str, str | None]:
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

    return jongseong, None


# FEAT: compat jaum to choseong pattern ("ㄱ" -> "[ㄱ가-깋]")
# FEAT: generate composite moum completion lookup table

if __name__ == "__main__":
    import ricecake.offset as o

    T = TypeVar("T")

    def mklookup(convert: Callable[[str], T], base: int, end: int) -> list[T]:
        return [convert(chr(code)) for code in range(base, end + 1)]

    CHOSEONG_TO_COMPAT_JAUM = mklookup(
        jamo_to_compat_jamo,
        o.MODERN_CHOSEONG_BASE,
        o.MODERN_CHOSEONG_END,
    )
    JONGSEONG_TO_COMPAT_JAUM = mklookup(
        jamo_to_compat_jamo,
        o.MODERN_JONGSEONG_BASE,
        o.MODERN_JONGSEONG_END,
    )

    COMPAT_JAUM_TO_CHOSEONG = mklookup(
        compat_jaum_to_choseong,
        o.MODERN_COMPAT_JAUM_BASE,
        o.MODERN_COMPAT_JAUM_END,
    )
    COMPAT_JAUM_TO_JONGSEONG = mklookup(
        compat_jaum_to_jongseong,
        o.MODERN_COMPAT_JAUM_BASE,
        o.MODERN_COMPAT_JAUM_END,
    )

    DECOMPOSE_JONGSEONG = mklookup(
        decompose_jongseong,
        o.MODERN_JONGSEONG_BASE,
        o.MODERN_JONGSEONG_END,
    )

    print(f"CHOSEONG_TO_COMPAT_JAUM = {CHOSEONG_TO_COMPAT_JAUM}\n")
    print(f"JONGSEONG_TO_COMPAT_JAUM = {JONGSEONG_TO_COMPAT_JAUM}\n")
    print(f"COMPAT_JAUM_TO_CHOSEONG = {COMPAT_JAUM_TO_CHOSEONG}\n")
    print(f"COMPAT_JAUM_TO_JONGSEONG = {COMPAT_JAUM_TO_JONGSEONG}\n")
    print(f"DECOMPOSE_JONGSEONG = {DECOMPOSE_JONGSEONG}\n")
