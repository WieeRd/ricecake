"""Generate Jamo <-> Compat Jamo conversion lookup tables.

* Jamo -> Compat Jamo
* Compat Jaum -> Jamo Choseong
* Compat Jaum -> Jamo Jongseong
* Compat Moum -> Jamo Jungseong
"""

from collections.abc import Iterator
import unicodedata as ud

# import ricecake.hangul as hg


def jamo_to_compat_jamo(jamo: str, /) -> str | None:
    """Maps a Jamo character to a Compatibility Jamo character."""
    # man I hate exceptions, where are my monadic types at?
    try:
        name = ud.name(jamo).split(" ")[-1]  # HANGUL CHOSEONG "KIYEOK"
        return ud.lookup(f"HANGUL LETTER {name}")
    except (ValueError, KeyError):
        return None


def compat_jaum_to_choseong(compat_jaum: str, /) -> str | None:
    """Maps a Compatibility Jaum character to a Jamo Choseong character."""
    # why can't you just return `None` instead of raising?
    try:
        name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
        return ud.lookup(f"HANGUL CHOSEONG {name}")
    except (ValueError, KeyError):
        return None


def compat_moum_to_jungseong(compat_moum: str, /) -> str | None:
    """Maps a Compatibility Moum character to a Jamo Jungseong character."""
    try:
        name = ud.name(compat_moum).split(" ")[-1]  # HANGUL LETTER "A"
        return ud.lookup(f"HANGUL JUNGSEONG {name}")
    except (ValueError, KeyError):
        return None


def compat_jaum_to_jongseong(compat_jaum: str, /) -> str | None:
    """Maps a Compatibility Jaum character to a Jamo Jongseong character."""
    try:
        name = ud.name(compat_jaum).split(" ")[-1]  # HANGUL LETTER "KIYEOK"
        return ud.lookup(f"HANGUL JONGSEONG {name}")
    except (ValueError, KeyError):
        return None


def decompose_jongseong(jongseong: str, /) -> tuple[str, str] | None:
    """Decomposes a composite Jongseong into tuple of 2 Jongseongs."""
    try:
        ud.name(jongseong).split(" ")[-1]  # HANGUL JONGSEONG "KIYEOK"
    except ValueError:
        return None

    # SSANG{jaum}, {jaum}-{jaum}


# FEAT: compat jaum to choseong pattern ("ㄱ" -> "[ㄱ가-깋]")
# FEAT: jaum decomposition ("ㄲ" -> ("ㄱ", "ㄱ"))
# FIX: ASAP: jungseong and jongseong does not have to be `Optional`

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
