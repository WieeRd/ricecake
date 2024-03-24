"""Generates regex patterns tailored for searching Korean texts."""

from dataclasses import dataclass

from .compose import get_jongseong
from .offset import JONGSEONG_COUNT, compat_jaum_offset, is_compat_jaum, is_syllable

__all__ = ["Searcher"]


CHOSEONG_SEARCH_PATTERN = [
    "[ㄱ가-깋]",
    "[ㄲ까-낗]",
    None,  # ㄳ
    "[ㄴ나-닣]",
    None,  # ㄵ
    None,  # ㄶ
    "[ㄷ다-딯]",
    "[ㄸ따-띻]",
    "[ㄹ라-맇]",
    None,  # ㄺ
    None,  # ㄻ
    None,  # ㄼ
    None,  # ㄽ
    None,  # ㄾ
    None,  # ㄿ
    None,  # ㅀ
    "[ㅁ마-밓]",
    "[ㅂ바-빟]",
    "[ㅃ빠-삫]",
    None,  # ㅄ
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
    # FEAT: LATER: sort-by, regex flags, filter, search/match/fullmatch

    def _search_pattern(self, c: str, /) -> str:
        if self.choseong_search and is_compat_jaum(c):
            return CHOSEONG_SEARCH_PATTERN[compat_jaum_offset(c)] or c

        if self.jongseong_completion and is_syllable(c) and get_jongseong(c) is None:
            return f"[{c}-{chr(ord(c) + JONGSEONG_COUNT)}]"

        return c

    @staticmethod
    def _incremental_pattern(c: str, /) -> str:
        # 1. Jaum
        # "ㄱ" -> "[ㄱ가-깋]"
        if is_compat_jaum(c):
            return CHOSEONG_SEARCH_PATTERN[compat_jaum_offset(c)] or c

        # 2. Syllable
        if not is_syllable(c):
            return c

        # 2.1. Has Jongseong
        jong = get_jongseong(c)
        if jong is not None:
            # 2.1.1. Single Jongseong
            # "일" -> "([일-잃]|이[ㄹ라-맇])"

            # 2.1.2. Composite Jongseong
            # "읽" -> "(읽|일[ㄱ가-깋])"
            raise NotImplementedError

        # 2.2. No Jongseong

        # 2.2.1. Composable Moum
        # "으" -> "[으-읳]"

        # 2.2.2. Complete Moum
        # "왜" -> "[왜-왷]"
        raise NotImplementedError
