"""Detection and (de)composition of Hangul unicode characters.

TODO:
    Explain the general concepts of Hangul unicode in the glossary section.

Glossary:
    - Hangul Syllable
    - Hangul Jamo
    - Hangul Compatibility Jamo
"""

from __future__ import annotations

__all__ = [
    "is_syllable",
    "is_jamo",
    "is_compat_jamo",
    "is_hangul",
]


SYLLABLE_START = 0xAC00
SYLLABLE_END = 0xD7A3

JAMO_START = 0x1100
JAMO_END = 0x11FF

COMPAT_JAMO_START = 0x3130
COMPAT_JAMO_END = 0x318F


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


# FEAT: add `is_modern_*()` variants
