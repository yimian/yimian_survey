# -*- coding: utf-8 -*-
import pickle


def get_dict_word_fre(corpus_path):
    word_all_num = 0
    dict_word_num = {}
    dict_word_fre = {}
    with open(corpus_path) as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            words = line.split(' ')
            for word in words:
                word_all_num += 1
                if word in dict_word_num:
                    dict_word_num[word] += 1
                else:
                    dict_word_num[word] = 1
    for word in dict_word_num:
        dict_word_fre[word] = dict_word_num[word] / word_all_num
    return word_all_num, dict_word_fre


def get_dict_word_weight(dict_word_fre, a=1e-3):
    if a <= 0:
        a = 1.0
    dict_word_weight = {}
    for word in dict_word_fre:
        dict_word_weight[word] = a / (a + dict_word_fre[word])
    return dict_word_weight


if __name__ == '__main__':
    tea_jieba_corpus_path = '/data/corpus/word2vec_corpus/tea_jieba.corpus'
    tea_word_all_num, tea_dict_word_fre = get_dict_word_fre(tea_jieba_corpus_path)
    print(tea_word_all_num)
    print(tea_dict_word_fre['好'])
    print(tea_dict_word_fre['的'])
    tea_dict_word_weight_path = '/data/sif_model/dict_word_weight.p'
    tea_dict_word_weight = get_dict_word_weight(tea_dict_word_fre)
    pickle.dump(tea_dict_word_weight, open(tea_dict_word_weight_path, 'wb'))
    print(tea_dict_word_weight['好'])
    print(tea_dict_word_weight['的'])
