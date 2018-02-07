# -*- coding: utf-8 -*-
import numpy as np
import jieba
import pickle
from sklearn.decomposition import TruncatedSVD
from numpy import dot
from numpy.linalg import norm


def get_weighted_embedding(text, params):
    """
    :param text: the text of sentence
    :param params: params class instance, which contain all the parameters
    :return: the weighted embedding for the sentence
    """
    # init the sentence embedding
    weighted_embedding = np.array([0.0] * params.w2v_size)
    words = jieba.cut(text)
    for word in words:
        if word in params.w2v_model:
            weighted_embedding += params.w2v_model[word] * params.dict_word_weight[word]
        else:
            # weighted_embedding += np.random.normal(size=params.w2v_size) * 0.001
            weighted_embedding += np.array([1.0] * params.w2v_size) * 0.001
    return weighted_embedding


def get_weighted_embedding_list(params):
    """
    :param params: params class instance, which contain all the parameters
    :return: the weighted embedding list of sentence list
    """
    weighted_embedding_list = []
    for sentence in params.sentence_list:
        weighted_embedding = get_weighted_embedding(sentence, params)
        weighted_embedding_list.append(weighted_embedding)
    return np.array(weighted_embedding_list)


def compute_pc(x, npc=1):
    """
    Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!
    :param x: x[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc
    """
    svd = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(x)
    return svd.components_


def remove_pc(x, npc=1):
    """
    Remove the projection on the principal components
    :param x: x[i,:] is a data point
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection
    """
    pc = compute_pc(x, npc)
    if npc == 1:
        xx = x - x.dot(pc.transpose()) * pc
    else:
        xx = x - x.dot(pc.transpose()).dot(pc)
    return xx


def build_pc_and_sif_embedding_list(params):
    """
    build the weighted embedding, principle component and sif embedding and save in pickle.

    :param params: params class instance, which contain all the parameters
    :return: null
    """
    weighted_embedding_list = get_weighted_embedding_list(params)
    pickle.dump(weighted_embedding_list, open(params.dump_weighted_embedding_path, 'wb'))
    print('Finish building the weighted embedding list of sentence list')
    pc = compute_pc(weighted_embedding_list)
    pickle.dump(pc, open(params.dump_pc_path, 'wb'))
    print('Finish building the pc')
    sif_embedding_list = remove_pc(weighted_embedding_list)
    pickle.dump(sif_embedding_list, open(params.dump_sif_embedding_list_path, 'wb'))
    print('Finish building the sif_embedding')


def my_cosine_similarity(v1, v2):
    cos_sim = dot(v1, v2) / (norm(v1) * norm(v2))
    return cos_sim[0]


def get_sif_embedding(text, params):
    """
    :param text: the text of sentence
    :param params: params class instance, which contain all the parameters
    :return: the SIF embedding for the sentence
    """
    # get the weighted embedding
    sentence_embedding = get_weighted_embedding(text, params)
    # remove the principle component from the sentence
    rmpc_sentence_embedding = sentence_embedding - sentence_embedding.dot(params.pc.transpose()) * params.pc
    return rmpc_sentence_embedding


def get_most_similar_k(text, k, params):
    """
    :param text: the text of sentence
    :param k: the number of return sentences
    :param params: params class instance, which contain all the parameters
    :return: the most similar k sentences and its cosine similarity
    """
    similarity_sentence_list = []
    sent_embedding = get_sif_embedding(text, params)
    # distance_list = np.array(list(map(lambda x: my_cosine_similarity(sent_emb, x), sentences_emb)))
    distance_list = np.array([my_cosine_similarity(sent_embedding, x) for x in params.sif_embedding])
    smallest_k_index = distance_list.argsort()[::-1][:k]
    for i in smallest_k_index:
        similarity_sentence_list.append([params.sentence_list[i], distance_list[i]])
    return similarity_sentence_list

