"""Generates regex patterns tailored for searching Korean texts."""

from dataclasses import dataclass

from .compose import decompose_jongseong, get_jongseong, get_jungseong, set_jongseong
from .convert import to_compat_jamo
from .offset import JONGSEONG_COUNT, compat_jaum_offset, is_compat_jaum, is_syllable

__all__ = ["Searcher"]


CHOSEONG_SEARCH_PATTERN = [
    "[ㄱ가-깋]",
    "[ㄲ까-낗]",
    "ㄳ",
    "[ㄴ나-닣]",
    "ㄵ",
    "ㄶ",
    "[ㄷ다-딯]",
    "[ㄸ따-띻]",
    "[ㄹ라-맇]",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "[ㅁ마-밓]",
    "[ㅂ바-빟]",
    "[ㅃ빠-삫]",
    "ㅄ",
    "[ㅅ사-싷]",
    "[ㅆ싸-앃]",
    "[ㅇ아-잏]",
    "[ㅈ자-짛]",
    "[ㅉ짜-찧]",
    "[ㅊ차-칳]",
    "[ㅋ카-킿]",
    "[ㅌ타-팋]",
    "[ㅍ파-핗]",
    "[ㅎ하-힣]",
]


# FIX: should take choseong instead of compat jaum this is weird
def choseong_pattern(compat_jaum: str) -> str:
    i = compat_jaum_offset(compat_jaum)
    return CHOSEONG_SEARCH_PATTERN[i]


def incremental_pattern(c: str, /) -> str:
    # 1. Jaum
    # "ㄱ" -> "[ㄱ가-깋]"
    if is_compat_jaum(c):
        return choseong_pattern(c)

    # 2. Syllable
    if not is_syllable(c):
        return c
    _cho, jung, jong = decompose(c)

    # 2.1. Has Jongseong
    if jong:
        first, second = decompose_jongseong(jong)

        # 2.1.1. Composite Jongseong
        # "읽" -> "(?:읽|일[ㄱ가-깋])"
        if second:
            jong_removed = set_jongseong(c, first)  # "일"
            cho_search = choseong_pattern(to_compat_jamo(second))  # "[ㄱ가-깋]"
            return f"(?:{c}|{jong_removed}{cho_search})"

        # 2.1.2. Single Jongseong
        # "일" -> "(?:[일-잃]|이[ㄹ라-맇])"
        jong_range = {
            "ᆨ": "ᆪ",
            "ᆫ": "ᆭ",
            "ᆯ": "ᆶ",
            "ᆸ": "ᆹ",
            "ᆺ": "ᆻ",
        }.get(jong)

        # "일" -> "[일-잃]" / "잊" -> "잊"
        jong_completion = f"[{c}-{set_jongseong(c, jong_range)}]" if jong_range else c
        jong_removed = set_jongseong(c, None)  # "이"
        cho_search = choseong_pattern(to_compat_jamo(jong))  # "[ㄹ라-맇]"
        return f"(?:{jong_completion}|{jong_removed}{cho_search})"

    # 2.2. No Jongseong

    # NOTE: Composability is based on Korean keyboard and IME behavior
    # | By definition, `ㅐ = ㅏ + ㅣ` and `ㅢ = ㅡ + ㅣ`.
    # | But `ㅐ` can be typed directly from a keyboard,
    # | and some IMEs do not support incrementally typing `ㅐ` as `ㅏ+ ㅣ`.
    # | `ㅢ` on the other hand can only be typed as `ㅡ + ㅣ`.
    # | Thus, `ㅡ` is considered composable while `ㅏ` is not.

    # 2.2.1. Composable Moum
    # "으" -> "[으-읳]"
    match jung:
        case "ᅩ":
            ...
        case "ᅮ":
            ...
        case "ᅳ":
            ...
        case _:
            ...

    # 2.2.2. Complete Moum
    # "왜" -> "[왜-왷]"
    raise NotImplementedError


# DOC: did you know? writing human language is a lot harder than programming language
# TEST: ASAP: speaking of docs, I haven't tested anything I coded so far.
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
    # FEAT: LATER: sort-by, regex flags, filter, search/match/fullmatch

    def _search_pattern(self, c: str, /) -> str:
        # "ㄱ" -> "[ㄱ가-깋]"
        if self.choseong_search and is_compat_jaum(c):
            return choseong_pattern(c)

        # "가" -> "[가-갛]"
        if self.jongseong_completion and is_syllable(c) and get_jongseong(c) is None:
            return f"[{c}-{set_jongseong(c, 'ᇂ')}]"

        return c
