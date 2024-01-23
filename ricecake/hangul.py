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


# https://en.wikipedia.org/wiki/Hangul_Jamo_(Unicode_block)
JAMO_START = 0x1100  # 'ᄀ'
JAMO_END = 0x11FF  # 'ᇿ'

JAMO_MODERN_CHOSEONG_START = 0x1100  # 'ᄀ'
JAMO_MODERN_CHOSEONG_END = 0x1112  # 'ᄒ'

JAMO_ARCHAIC_CHOSEONG_START = 0x1113  # 'ᄓ'
JAMO_ARCHAIC_CHOSEONG_END = 0x115E  # 'ᅞ'

JAMO_CHOSEONG_FILLER = 0x115F
JAMO_JONGSEONG_FILLER = 0x1160

JAMO_MODERN_MOUM_START = 0x1161  # 'ᅡ'
JAMO_MODERN_MOUM_END = 0x1175  # 'ᅵ'

JAMO_ARCHAIC_MOUM_START = 0x1176  # 'ᅶ'
JAMO_ARCHAIC_MOUM_END = 0x11A7  # 'ᆧ'

JAMO_MODERN_JONGSEONG_START = 0x11A8  # 'ᆨ'
JAMO_MODERN_JONGSEONG_END = 0x11C2  # 'ᇂ'

JAMO_ARCHAIC_JONGSEONG_START = 0x11C3  # 'ᇃ'
JAMO_ARCHAIC_JONGSEONG_END = 0x11FF  # 'ᇿ'


# https://en.wikipedia.org/wiki/Hangul_Syllables
SYLLABLE_START = 0xAC00  # '가'
SYLLABLE_END = 0xD7A3  # '힣'

CHOSEONG_MULTIPLIER = 588
MOUM_MULTIPLIER = 28
JONGSEONG_MULTIPLIER = 1


# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
COMPAT_JAMO_START = 0x3130  # 'ㄱ' - 1 (U+3130 is reserved)
COMPAT_JAMO_END = 0x318F  # 'ㆎ' + 1 (U+318F is reserved)

COMPAT_JAMO_MODERN_JAUM_START = 0x3131  # 'ㄱ'
COMPAT_JAMO_MODERN_JAUM_END = 0x314E  # 'ㅎ'

COMPAT_JAMO_MODERN_MOUM_START = 0x314F  # 'ㅏ'
COMPAT_JAMO_MODERN_MOUM_END = 0x314F  # 'ㅣ'

COMPAT_JAMO_HANGUL_FILLER = 0x3164

COMPAT_JAMO_ARCHAIC_JAUM_START = 0x3165  # 'ㅥ'
COMPAT_JAMO_ARCHAIC_JAUM_END = 0x3186  # 'ㆎ'

COMPAT_JAMO_ARCHAIC_MOUM_START = 0x3187  # 'ㆇ'
COMPAT_JAMO_ARCHAIC_MOUM_END = 0x318E  # 'ㆎ'

# FEAT: MAYBE: should I support Jamo Extended A, B and halfwidth variants?


def is_syllable(c: str, /) -> bool:
    """Checks if a character is a Hangul Syllable."""
    return SYLLABLE_START <= ord(c) <= SYLLABLE_END


def is_jamo(c: str, /) -> bool:
    """Checks if a character is a Hangul Jamo.

    !!! warn

        **This will NOT detect standalone Jamo characters typed with keyboards.**
        Make sure to read the glossary section of the module docs and understand
        the difference between Hangul Jamo and Hangul *Compatibility* Jamo.
    """
    return JAMO_START <= ord(c) <= JAMO_END


def is_compat_jamo(c: str, /) -> bool:
    """Checks if a character is a Hangul Compatibility Jamo."""
    return COMPAT_JAMO_START <= ord(c) <= COMPAT_JAMO_END


def is_hangul(c: str, /) -> bool:
    """Checks if a character is a Hangul character.

    Equivalent to `is_syllable(c) or is_jamo(c) or is_compat_jamo(c)`.

    !!! note

        This does not include Hangul Jamo Extended A and B.
    """
    code = ord(c)
    return (
        SYLLABLE_START <= code <= SYLLABLE_END
        or COMPAT_JAMO_START <= code <= COMPAT_JAMO_END
        or JAMO_START <= code <= JAMO_END
    )
