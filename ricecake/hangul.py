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

from collections.abc import Iterator


# https://en.wikipedia.org/wiki/Hangul_Syllables
SYLLABLE_START = 0xAC00  # '가'
SYLLABLE_END = 0xD7A3  # '힣'

CHOSEONG_MULTIPLIER = 588
MOUM_MULTIPLIER = 28
JONGSEONG_MULTIPLIER = 1


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
# FIX: find a shorter but reasonable names for constants


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


# fmt: off
_COMPAT_JAMO_CHOSEONG_PATTERN = [
    "[ㄱ가-깋]",  # "ㄱ"
    "[ㄲ까-낗]",  # "ㄲ"
    None,         # "ㄳ"
    "[ㄴ나-닣]",  # "ㄴ"
    None,         # "ㄵ"
    None,         # "ㄶ"
    "[ㄷ다-딯]",  # "ㄷ"
    "[ㄸ따-띻]",  # "ㄸ"
    "[ㄹ라-맇]",  # "ㄹ"
    None,         # "ㄺ"
    None,         # "ㄻ"
    None,         # "ㄼ"
    None,         # "ㄽ"
    None,         # "ㄾ"
    None,         # "ㄿ"
    None,         # "ㅀ"
    "[ㅁ마-밓]",  # "ㅁ"
    "[ㅂ바-빟]",  # "ㅂ"
    "[ㅃ빠-삫]",  # "ㅃ"
    None,         # "ㅄ"
    "[ㅅ사-싷]",  # "ㅅ"
    "[ㅆ싸-앃]",  # "ㅆ"
    "[ㅇ아-잏]",  # "ㅇ"
    "[ㅈ자-짛]",  # "ㅈ"
    "[ㅉ짜-찧]",  # "ㅉ"
    "[ㅊ차-칳]",  # "ㅊ"
    "[ㅋ카-킿]",  # "ㅋ"
    "[ㅌ타-팋]",  # "ㅌ"
    "[ㅍ파-핗]",  # "ㅍ"
    "[ㅎ하-힣]",  # "ㅎ"
]
# fmt: on


def search_pattern(
    text: str,
    /,
    *,
    choseong_search: bool = True,
    jongseong_completion: bool = True,
    incremental: bool = True,
) -> Iterator[str]:
    """Generates a regex pattern tailored for searching Hangul texts.

    Examples: Coming soon:tm:

    Args:
        text: ...
        choseong_search: ...
        jongseong_completion: ...
        incremental: ...
    """
    for c in text:
        if jongseong_completion and is_syllable(c):
            # checks if the syllable is missing a jongseong
            # if so, yield a pattern that matches any jongseong
            # e.g. "슈" -> "[슈-슣]" / "슉" -> "슉"
            code = ord(c)
            if (code - SYLLABLE_START) % MOUM_MULTIPLIER == 0:
                yield f"[{c}-{chr(code + MOUM_MULTIPLIER - 1)}]"

        elif choseong_search and is_compat_jamo(c):
            # compat jamo cannot be 1:1 mapped to jamo or syllable using algorithm
            # because jamo separates jongseong-only jaums while compat jamo does not
            # instead, consult the lookup table and yield a pattern that matches
            # choseong itself, or any syllable that starts with the choseong
            offset = ord(c) - COMPAT_JAMO_START
            yield _COMPAT_JAMO_CHOSEONG_PATTERN[offset] or c

        elif is_jamo(c):
            raise ValueError("Hangul Jamo and NFD-normalized string are not supported")

        yield c

    if not (incremental and text):
        return

    # FEAT: get the last character, and do either jongseong completion or choseong search
    raise NotImplementedError
