"""Generates regex patterns tailored for searching Korean texts."""

import re
from collections.abc import Iterator
from dataclasses import dataclass

from . import offset as o

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


# DOC: did you know? writing human language is a lot harder than programming language
# TEST: speaking of docs, I haven't tested anything I coded so far.
# | I should add example sections with doctests at some point
# | when is that some point? who knows.
@dataclass(kw_only=True)
class Searcher:
    """Fuzzy & incremental search for Korean texts.

    Attributes:
        choseong_search: Match Jaum with all syllables using that Jaum as a Choseong.
        jongseong_completion: Documentation is hard.
        incremental: I'll come back later.
        fuzzy: Hopefully.
    """

    choseong_search: bool
    jongseong_completion: bool
    incremental: bool
    fuzzy: bool

    def _search_pattern(self, text: str, /) -> Iterator[str]:
        """Generates regex patterns for each character in the text."""
        for c in re.escape(text):
            code = ord(c)

            # FEAT: LATER: composite jamo completion e.g. "우" -> "위", "일" -> "읽"
            if self.jongseong_completion and o.is_syllable(c):
                # checks if the syllable is missing a jongseong
                # if so, yield a pattern that matches any jongseong
                # e.g. "슈" -> "[슈-슣]" / "슉" -> "슉"
                if (code - o.SYLLABLE_BASE) % o.JUNGSEONG_COEF == 0:
                    yield f"[{c}-{chr(code + o.JUNGSEONG_COEF - 1)}]"

            elif (
                self.choseong_search
                and o.MODERN_COMPAT_JAUM_BASE <= code <= o.MODERN_COMPAT_JAUM_END
            ):
                # compat jamo cannot be 1:1 mapped to jamo or syllable using algorithm
                # because jamo separates jongseong-only jaums while compat jamo does not
                # instead, consult the lookup table and yield a pattern that matches
                # choseong itself, or any syllable that starts with the choseong
                offset = ord(c) - o.MODERN_COMPAT_JAUM_BASE
                yield _COMPAT_JAMO_CHOSEONG_PATTERN[offset] or c

            elif o.is_jamo(c):
                # FEAT: preprocess text with `re.escape()` and `unicodedata.normalize("NFC", ...)`
                # | should this be the caller's responsibility or this function's?
                raise ValueError(
                    "Hangul Jamo and NFD-normalized string are not supported"
                )

            yield c

        if not (self.incremental and text):
            return

        # FEAT: get the last character, and do either jongseong completion or choseong search
        raise NotImplementedError
