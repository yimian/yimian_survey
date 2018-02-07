# -*- coding: utf-8 -*-
from pypinyin import lazy_pinyin
from Levenshtein import distance

get_pinyin = lazy_pinyin
keywords = []

with open('./corpus.txt') as f:
    for line in f.readlines():
        keywords.append(line.replace('\n', ''))

len_keywords = [len(keyword) for keyword in keywords]
max_len = max(len_keywords)
min_len = min(len_keywords)
keywords_py = ["".join(get_pinyin(keyword)) for keyword in keywords]


def correct_by_subchar(text):
    text_len = len(text)
    chars = list(text)
    pys = get_pinyin(text)
    for keyword_len in range(min_len, max_len + 1):
        if keyword_len <= text_len:
            for keyword_bias in range(text_len - keyword_len + 1):
                sub_py = "".join(pys[keyword_bias: keyword_bias + keyword_len])
                for keyword_py in keywords_py:
                    if distance(sub_py, keyword_py) <= 2:
                        chars[keyword_bias: keyword_bias + keyword_len] = list(keywords[keywords_py.index(keyword_py)])
    return "".join(chars)


def correct_use_levenshtein2(text):
    text_len = len(text)
    py = get_pinyin(text)
    chars = list(text)
    white_list = [0] * text_len
    kw_len = max_len
    while kw_len >= 2:
        kw_bias = 0
        while kw_bias + kw_len <= text_len:
            if 1 not in white_list[kw_bias: kw_bias + kw_len]:
                # print(kw_bias, kw_len, text_len)
                kw = ''.join(chars[kw_bias: kw_bias + kw_len])
                # print('kw: ', kw)
                one_step = True
                if kw in keywords:
                    one_step = False
                else:
                    candidate = ''.join(py[kw_bias:kw_bias + kw_len])
                    # print('candidate: ', candidate)
                    for keyword_py in keywords_py:
                        if distance(keyword_py, candidate) < 2:
                            chars[kw_bias:kw_bias + kw_len] = list(keywords[keywords_py.index(keyword_py)])
                            one_step = False
                if one_step:
                    kw_bias += 1
                else:
                    white_list[kw_bias: kw_bias + kw_len] = [1] * kw_len
                    kw_bias += kw_len
            else:
                kw_bias += 1
        kw_len -= 1
    return ''.join(chars)


if __name__ == '__main__':
    text_test = '霍山黄芽茶说'
    text_corrected = correct_use_levenshtein2(text_test)
    print(text_corrected)
