# -*- coding: utf-8 -*-
import pickle
import gensim


class Params(object):
    def __init__(self):
        self.w2v_size = 0

        self.dump_pc_path = ''
        self.dump_weighted_embedding_path = ''
        self.dump_sif_embedding_list_path = ''

        self.load_pc_path = ''
        self.load_sentence_list_path = ''
        self.load_sif_embedding_path = ''
        self.load_dict_word_weight_path = ''
        self.load_w2v_model_path = ''

        self.pc = None
        self.sentence_list = None
        self.sif_embedding = None
        self.dict_word_weight = None
        self.w2v_model = None

    def load_model(self):
        if self.load_pc_path:
            self.pc = pickle.load(open(self.load_pc_path, 'rb'))
        else:
            print('There is not pc path')

        if self.load_sentence_list_path:
            sentence_list = []
            with open(self.load_sentence_list_path) as f:
                for line in f.readlines():
                    line = line.replace('\n', '')
                    sentence_list.append(line)
            self.sentence_list = sentence_list
        else:
            print('There is not sentence list path')

        if self.load_sif_embedding_path:
            self.sif_embedding = pickle.load(open(self.load_sif_embedding_path, 'rb'))
        else:
            print('There is not sif embedding path')
        if self.load_dict_word_weight_path:
            self.dict_word_weight = pickle.load(open(self.load_dict_word_weight_path, 'rb'))
        else:
            print('There is not dict_word_weight path')
        if self.load_w2v_model_path:
            self.w2v_model = gensim.models.Word2Vec.load(self.load_w2v_model_path)
        else:
            print('There is not w2v model path')

    def tea_init(self):
        self.w2v_size = 200
        self.dump_pc_path = '/data/sif_model/pc.p'
        self.dump_weighted_embedding_path = '/data/sif_model/weighted_embedding_path'
        self.dump_sif_embedding_list_path = '/data/sif_model/sif_embedding.p'
        self.load_pc_path = '/data/sif_model/pc.p'
        self.load_sentence_list_path = '/data/sif_model/tea_question.csv'
        self.load_sif_embedding_path = '/data/sif_model/sif_embedding.p'
        self.load_dict_word_weight_path = '/data/sif_model/dict_word_weight.p'
        self.load_w2v_model_path = '/data/w2v_model/tea/tea_jieba.model'
        self.load_model()


params_o = Params()
params_o.tea_init()
