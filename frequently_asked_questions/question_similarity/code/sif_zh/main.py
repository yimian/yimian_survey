# -*- coding: utf-8 -*-
from src.params import params_o
from src.sif_embedding import build_pc_and_sif_embedding_list
from src.sif_embedding import get_most_similar_k

if __name__ == '__main__':
    # build and reload the models only if in the first time you
    build_pc_and_sif_embedding_list(params_o)
    params_o.load_model()

    test_sent = '是不是等级越高的茶越好？'
    similarity_sentences = get_most_similar_k(test_sent, 5, params_o)
    for i in similarity_sentences:
        print(i)
