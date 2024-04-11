"""Identifying Unicode Hangul Characters.

- `*_BASE` & `*_END`: Hangul Unicode codepoint ranges
- `is_*()`: Detect Hangul characters
- `*_offset()`: Calculate codepoint offsets
"""

# https://en.wikipedia.org/wiki/Hangul_Syllables
SYLLABLE_BASE = 0xAC00  # '가'
SYLLABLE_END = 0xD7A3  # '힣'


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


CHOSEONG_COUNT = MODERN_CHOSEONG_END - MODERN_CHOSEONG_BASE + 1
JUNGSEONG_COUNT = MODERN_JUNGSEONG_END - MODERN_JUNGSEONG_BASE + 1
JONGSEONG_COUNT = MODERN_JONGSEONG_END - MODERN_JONGSEONG_BASE + 1 + 1

CHOSEONG_COEF = JUNGSEONG_COUNT * JONGSEONG_COUNT
JUNGSEONG_COEF = JONGSEONG_COUNT
JONGSEONG_COEF = 1


# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
COMPAT_JAMO_BASE = 0x3130  # 'ㄱ' - 1 (U+3130 is reserved)
COMPAT_JAMO_END = 0x318F  # 'ㆎ' + 1 (U+318F is reserved)

MODERN_COMPAT_JAUM_BASE = 0x3131  # 'ㄱ'
MODERN_COMPAT_JAUM_END = 0x314E  # 'ㅎ'

MODERN_COMPAT_MOUM_BASE = 0x314F  # 'ㅏ'
MODERN_COMPAT_MOUM_END = 0x3163  # 'ㅣ'

COMPAT_HANGUL_FILLER = 0x3164

ARCHAIC_COMPAT_JAUM_BASE = 0x3165  # 'ㅥ'
ARCHAIC_COMPAT_JAUM_END = 0x3186  # 'ㆎ'

ARCHAIC_COMPAT_MOUM_BASE = 0x3187  # 'ㆇ'
ARCHAIC_COMPAT_MOUM_END = 0x318E  # 'ㆎ'


# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-A
JAMO_EXTENDED_A_BASE = 0xA960
JAMO_EXTENDED_A_END = 0xA97F

# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-B
JAMO_EXTENDED_B_BASE = 0xD7B0
JAMO_EXTENDED_B_END = 0xD7FF

# https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
HALFWIDTH_JAMO_BASE = 0xFFA0
HALFWIDTH_JAMO_END = 0xFFDC


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


def is_compat_jaum(c: str, /) -> bool:
    """Checks if a character is a modern Hangul Compatibility Jamo Jaum."""
    return MODERN_COMPAT_JAUM_BASE <= ord(c) <= MODERN_COMPAT_JAUM_END


def is_compat_moum(c: str, /) -> bool:
    """Checks if a character is a modern Hangul Compatibility Jamo Moum."""
    return MODERN_COMPAT_MOUM_BASE <= ord(c) <= MODERN_COMPAT_MOUM_END


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


def syllable_offset(c: str, /) -> int:
    """Calculates the offset of a Hangul Syllable character.

    Raises:
        ValueError: If the character is not a Hangul Syllable.
    """
    code = ord(c)
    if SYLLABLE_BASE <= code <= SYLLABLE_END:
        return code - SYLLABLE_BASE
    raise ValueError("expected a Hangul Syllable character")


def jamo_offset(c: str, /) -> int:
    """Calculates the offset of a Hangul Jamo character.

    Raises:
        ValueError: If the character is not a Hangul Jamo.
    """
    code = ord(c)
    if JAMO_BASE <= code <= JAMO_END:
        return code - JAMO_BASE
    raise ValueError("expected a Hangul Jamo character")


def choseong_offset(c: str, /) -> int:
    """Calculates the Choseong offset of a modern Hangul Jamo character.

    Raises:
        ValueError: If the character is not a modern Hangul Jamo Choseong.
    """
    code = ord(c)
    if MODERN_CHOSEONG_BASE <= code <= MODERN_CHOSEONG_END:
        return code - MODERN_CHOSEONG_BASE
    raise ValueError("expected a modern Hangul Jamo Choseong character")


def jungseong_offset(c: str, /) -> int:
    """Calculates the Jungseong offset of a modern Hangul Jamo character.

    Raises:
        ValueError: If the character is not a modern Hangul Jamo Jungseong.
    """
    code = ord(c)
    if MODERN_JUNGSEONG_BASE <= code <= MODERN_JUNGSEONG_END:
        return code - MODERN_JUNGSEONG_BASE
    raise ValueError("expected a modern Hangul Jamo Jungseong character")


def jongseong_offset(c: str, /) -> int:
    """Calculates the Jungseong offset of a modern Hangul Jamo character.

    Note that unlike Choseong and Jungseong, Jongseong offset starts from 1.
    This is because offset 0 is used to denote the lack of Jongseong
    when composing a Hangul Syllable from Jamo offsets and vice versa.

    !!! warn
        
        When composing a Hangul Syllable from Cho/Jung/Jongseong offsets,
        you must add 1 to the Jongseong offset because 0 is used to denote
        the lack of Jongseong. e.g. `SYL = (CHO * 588) + (JUNG * 28) + (JONG + 1)`
        Using the `compose()` API is recommended to avoid this caveat.

    Raises:
        ValueError: If the character is not a modern Hangul Jamo Jongseong.
    """
    code = ord(c)
    if MODERN_JONGSEONG_BASE <= code <= MODERN_JONGSEONG_END:
        return code - MODERN_JONGSEONG_BASE
    raise ValueError("expected a modern Hangul Jamo Jongseong character")


def compat_jamo_offset(c: str, /) -> int:
    """Calculates the offset of a Hangul Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a Hangul Compatibility Jamo.
    """
    code = ord(c)
    if COMPAT_JAMO_BASE <= code <= COMPAT_JAMO_END:
        return code - COMPAT_JAMO_BASE
    raise ValueError("expected a Hangul Compatibility Jamo character")


def compat_jaum_offset(c: str, /) -> int:
    """Calculates the Jaum offset of a modern Hangul Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a modern Hangul Compatibility Jamo Jaum.
    """
    code = ord(c)
    if MODERN_COMPAT_JAUM_BASE <= code <= MODERN_COMPAT_JAUM_END:
        return code - MODERN_COMPAT_JAUM_BASE
    raise ValueError("expected a modern Hangul Compatibility Jamo Jaum character")


def compat_moum_offset(c: str, /) -> int:
    """Calculates the Moum offset of a modern Hangul Compatibility Jamo character.

    Raises:
        ValueError: If the character is not a modern Hangul Compatibility Jamo Moum.
    """
    code = ord(c)
    if MODERN_COMPAT_MOUM_BASE <= code <= MODERN_COMPAT_MOUM_END:
        return code - MODERN_COMPAT_MOUM_BASE
    raise ValueError("expected a modern Hangul Compatibility Jamo Moum character")
