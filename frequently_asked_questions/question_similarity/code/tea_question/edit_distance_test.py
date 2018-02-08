from Levenshtein import *
import numpy as np

lines = open('./tea_question.csv', encoding='utf-8').readlines()

def get_most_similar_k(test_str, k):
    # 求出 test_str 与所有句子的 edit distance，并转成 ndarray，方便调用内置方法
    distance_list = np.array(list(map(lambda x: distance(test_str, x), lines)))
    # 找到最小的前 k 个 distance 的下标
    smallest_k_index = distance_list.argsort()[0: k]
    for i in smallest_k_index:
        print(lines[i], distance_list[i])

test_str_1 = '如何鉴别茶叶品质的好坏？\n'
get_most_similar_k(test_str_1, 3)


