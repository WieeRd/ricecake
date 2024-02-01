"""Generates regex patterns tailored for searching Korean texts."""

import re
from collections.abc import Iterator

from . import hangul as hg

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
    for c in re.escape(text):
        code = ord(c)

        # FEAT: LATER: composite jamo completion e.g. "우" -> "위", "일" -> "읽"
        if jongseong_completion and hg.is_syllable(c):
            # checks if the syllable is missing a jongseong
            # if so, yield a pattern that matches any jongseong
            # e.g. "슈" -> "[슈-슣]" / "슉" -> "슉"
            if (code - hg.SYLLABLE_BASE) % hg.JUNGSEONG_COEF == 0:
                yield f"[{c}-{chr(code + hg.JUNGSEONG_COEF - 1)}]"

        elif (
            choseong_search
            and hg.COMPAT_MODERN_JAUM_BASE <= code <= hg.COMPAT_MODERN_JAUM_END
        ):
            # compat jamo cannot be 1:1 mapped to jamo or syllable using algorithm
            # because jamo separates jongseong-only jaums while compat jamo does not
            # instead, consult the lookup table and yield a pattern that matches
            # choseong itself, or any syllable that starts with the choseong
            offset = ord(c) - hg.COMPAT_MODERN_JAUM_BASE
            yield _COMPAT_JAMO_CHOSEONG_PATTERN[offset] or c

        elif hg.is_jamo(c):
            # FEAT: preprocess text with `re.escape()` and `unicodedata.normalize("NFC", ...)`
            # | should this be the caller's responsibility or this function's?
            raise ValueError("Hangul Jamo and NFD-normalized string are not supported")

        yield c

    if not (incremental and text):
        return

    # FEAT: get the last character, and do either jongseong completion or choseong search
    raise NotImplementedError
