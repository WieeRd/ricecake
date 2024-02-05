"""Detection and (de)composition of Hangul unicode characters.

Todo:
    Explain the general concepts of Hangul unicode in the glossary section.

Glossary:
    - Hangul Syllable
    - Hangul Jamo
    - Hangul Compatibility Jamo
"""

__all__ = [
    "is_syllable",
    "is_jamo",
    "is_compat_jamo",
    "is_hangul",
]

# https://en.wikipedia.org/wiki/Hangul_Syllables
SYLLABLE_BASE = 0xAC00  # '가'
SYLLABLE_END = 0xD7A3  # '힣'

CHOSEONG_COEF = 588
JUNGSEONG_COEF = 28
JONGSEONG_COEF = 1


# https://en.wikipedia.org/wiki/Hangul_Jamo_(Unicode_block)
JAMO_BASE = 0x1100  # 'ᄀ'
JAMO_END = 0x11FF  # 'ᇿ'

MODERN_CHOSEONG_BASE = 0x1100  # 'ᄀ'
MODERN_CHOSEONG_END = 0x1112  # 'ᄒ'

ARCHAIC_CHOSEONG_BASE = 0x1113  # 'ᄓ'
ARCHAIC_CHOSEONG_END = 0x115E  # 'ᅞ'

CHOSEONG_FILLER = 0x115F
JONGSEONG_FILLER = 0x1160

MODERN_JUNGSEONG_BASE = 0x1161  # 'ᅡ'
MODERN_JUNGSEONG_END = 0x1175  # 'ᅵ'

ARCHAIC_JUNGSEONG_BASE = 0x1176  # 'ᅶ'
ARCHAIC_JUNGSEONG_END = 0x11A7  # 'ᆧ'

MODERN_JONGSEONG_BASE = 0x11A8  # 'ᆨ'
MODERN_JONGSEONG_END = 0x11C2  # 'ᇂ'

ARCHAIC_JONGSEONG_BASE = 0x11C3  # 'ᇃ'
ARCHAIC_JONGSEONG_END = 0x11FF  # 'ᇿ'


# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
COMPAT_JAMO_BASE = 0x3130  # 'ㄱ' - 1 (U+3130 is reserved)
COMPAT_JAMO_END = 0x318F  # 'ㆎ' + 1 (U+318F is reserved)

COMPAT_MODERN_JAUM_BASE = 0x3131  # 'ㄱ'
COMPAT_MODERN_JAUM_END = 0x314E  # 'ㅎ'

COMPAT_MODERN_MOUM_BASE = 0x314F  # 'ㅏ'
COMPAT_MODERN_MOUM_END = 0x3163  # 'ㅣ'

COMPAT_HANGUL_FILLER = 0x3164

COMPAT_ARCHAIC_JAUM_BASE = 0x3165  # 'ㅥ'
COMPAT_ARCHAIC_JAUM_END = 0x3186  # 'ㆎ'

COMPAT_ARCHAIC_MOUM_BASE = 0x3187  # 'ㆇ'
COMPAT_ARCHAIC_MOUM_END = 0x318E  # 'ㆎ'


# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-A
JAMO_EXTENDED_A_BASE = 0xA960
JAMO_EXTENDED_A_END = 0xA97F

# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-B
JAMO_EXTENDED_B_BASE = 0xD7B0
JAMO_EXTENDED_B_END = 0xD7FF

# https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
HALFWIDTH_JAMO_BASE = 0xFFA0
HALFWIDTH_JAMO_END = 0xFFDC


# FIX: LATER: `*_offset() -> int | None`

# PERF: direct string comparison might be faster than invoking `ord`
# | `"ㄱ" <= c <= "ㅎ"` vs `0x3131 <= ord(c) <= 0x314E`


def is_syllable(c: str, /) -> bool:
    """Checks if a character is a Hangul Syllable."""
    return SYLLABLE_BASE <= ord(c) <= SYLLABLE_END


def is_jamo(c: str, /) -> bool:
    """Checks if a character is a Hangul Jamo.

    !!! warn

        **This will NOT detect standalone Jamo characters typed with keyboards.**
        Make sure to read the glossary section of the module docs and understand
        the difference between Hangul Jamo and Hangul *Compatibility* Jamo.
    """
    return JAMO_BASE <= ord(c) <= JAMO_END


def is_compat_jamo(c: str, /) -> bool:
    """Checks if a character is a Hangul Compatibility Jamo."""
    return COMPAT_JAMO_BASE <= ord(c) <= COMPAT_JAMO_END


def is_hangul(c: str, /) -> bool:
    """Checks if a character is a Hangul character.

    Equivalent to `is_syllable(c) or is_jamo(c) or is_compat_jamo(c)`.

    !!! note

        This does not include Hangul Jamo Extended A and B.
    """
    code = ord(c)
    return (
        SYLLABLE_BASE <= code <= SYLLABLE_END
        or COMPAT_JAMO_BASE <= code <= COMPAT_JAMO_END
        or JAMO_BASE <= code <= JAMO_END
    )
