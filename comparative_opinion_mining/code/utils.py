import config
import os


def get_pre_corpus_path(path):
    return os.path.join(config.PRE_CORPUS_PATH, path)


def get_corpus_path(path):
    return os.path.join(config.CORPUS_PATH, path)


def get_model_path(path):
    return os.path.join(config.MODEL_PATH, path)


def get_w2v_model_path(path):
    return os.path.join(config.W2V_MODEL_PATH, path)
