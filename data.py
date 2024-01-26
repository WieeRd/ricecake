"""Generate Jamo <-> Compat Jamo conversion lookup tables.

* Jamo -> Compat Jamo
* Compat Jaum -> Jamo Choseong
* Compat Jaum -> Jamo Jongseong
* Compat Moum -> Jamo Jungseong
"""

import unicodedata as ud

import ricecake.hangul as hg

# print(f'"\\u{ord(compat_char):X}",  # {jamo_char} -> {compat_char}')
# print(f"None,      # {jamo_char}")

jamo_to_compat_jamo = []
for code in range(hg.JAMO_START, hg.JAMO_END + 1):
    jamo = chr(code)
    name = ud.name(jamo).split()[-1]  # HANGUL CHOSEONG "KIYEOK"

    try:
        compat_jamo = ud.lookup(f"HANGUL LETTER {name}")
    except KeyError:
        compat_jamo = None

    jamo_to_compat_jamo.append(compat_jamo)


compat_jaum_to_choseong = []
compat_jaum_to_jongseong = []
for code in range(hg.COMPAT_MODERN_JAUM_START, hg.COMPAT_MODERN_JAUM_END + 1):
    jaum = chr(code)
    name = ud.name(jaum).split()[-1]  # HANGUL LETTER "KIYEOK"

    # man I hate exceptions, where are my monads at?
    try:
        choseong = ud.lookup(f"HANGUL CHOSEONG {name}")
    except KeyError:
        choseong = None

    # why can't you just return None instead of raising KeyError
    try:
        jongseong = ud.lookup(f"HANGUL JONGSEONG {name}")
    except KeyError:
        jongseong = None

    compat_jaum_to_choseong.append(choseong)
    compat_jaum_to_jongseong.append(jongseong)


compat_moum_to_jungseong = []
for code in range(hg.COMPAT_MODERN_MOUM_START, hg.COMPAT_MODERN_MOUM_END + 1):
    moum = chr(code)
    name = ud.name(moum).split()[-1]  # HANGUL LETTER "A"

    try:
        jungseong = ud.lookup(f"HANGUL JUNGSEONG {name}")
    except KeyError:  # <- its life is literally as valuable as a summer ant
        jungseong = None

    compat_moum_to_jungseong.append(jungseong)

# FEAT: compat jamo to pattern ("ㄱ" -> "[ㄱ가-깋]")

print(f"JAMO_TO_COMPAT_JAMO = {jamo_to_compat_jamo}")
print(f"COMPAT_JAUM_TO_CHOSEONG = {compat_jaum_to_choseong}")
print(f"COMPAT_MOUM_TO_JUNGSEONG = {compat_moum_to_jungseong}")
print(f"COMPAT_JAUM_TO_JONGSEONG = {compat_jaum_to_jongseong}")
