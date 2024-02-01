"""Generate Jamo <-> Compat Jamo conversion lookup tables.

* Jamo -> Compat Jamo
* Compat Jaum -> Jamo Choseong
* Compat Jaum -> Jamo Jongseong
* Compat Moum -> Jamo Jungseong
"""

import unicodedata as ud
from collections.abc import Iterator


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


# FEAT: jaum decomposition ("ㄲ" -> ("ㄱ", "ㄱ"))
def decompose_jongseong(jongseong: str, /) -> tuple[str, str] | None:
    """Decomposes a composite Jongseong into tuple of 2 Jongseongs."""
    _name = ud.name(jongseong).split(" ")[-1]  # HANGUL JONGSEONG "KIYEOK"

    # FEAT: SSANG{jaum}, {jaum}-{jaum}
    raise NotImplementedError


# FEAT: compat jaum to choseong pattern ("ㄱ" -> "[ㄱ가-깋]")

if __name__ == "__main__":
    import ricecake.hangul as hg

    def _c(start: int, stop: int) -> Iterator[str]:
        return map(chr, range(start, stop))

    JAMO_TO_COMPAT_JAMO = [
        jamo_to_compat_jamo(j) for j in _c(hg.JAMO_BASE, hg.JAMO_END + 1)
    ]
    COMPAT_JAUM_TO_CHOSEONG = [
        compat_jaum_to_choseong(cj)
        for cj in _c(hg.COMPAT_MODERN_JAUM_BASE, hg.COMPAT_MODERN_JAUM_END + 1)
    ]
    COMPAT_MOUM_TO_JUNGSEONG = [
        compat_moum_to_jungseong(cm)
        for cm in _c(hg.COMPAT_MODERN_MOUM_BASE, hg.COMPAT_MODERN_MOUM_END + 1)
    ]
    COMPAT_JAUM_TO_JONGSEONG = [
        compat_jaum_to_jongseong(cj)
        for cj in _c(hg.COMPAT_MODERN_JAUM_BASE, hg.COMPAT_MODERN_JAUM_END + 1)
    ]

    print(f"JAMO_TO_COMPAT_JAMO = {JAMO_TO_COMPAT_JAMO}\n")
    print(f"COMPAT_JAUM_TO_CHOSEONG = {COMPAT_JAUM_TO_CHOSEONG}\n")
    print(f"COMPAT_MOUM_TO_JUNGSEONG = {COMPAT_MOUM_TO_JUNGSEONG}\n")
    print(f"COMPAT_JAUM_TO_JONGSEONG = {COMPAT_JAUM_TO_JONGSEONG}\n")
