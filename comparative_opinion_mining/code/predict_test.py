import numpy as np
import random
import jieba
import time

import gensim
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras import regularizers
from keras.layers import Embedding
from keras.layers import LSTM
from keras.preprocessing import text, sequence

# Input parameters
max_features = 50000
max_len = 50
embedding_size = 400
border_mode = 'same'
dropout = 0.5
l2_regularization = 0.2


import keras
from keras.preprocessing import text, sequence
import jieba
import numpy as np

w2v_model = gensim.models.Word2Vec.load('movie.model')
model = keras.models.load_model('compa_sent.model')

l1 = []
l2 = []
pos_f_name, neg_f_name = './data/c_pos.txt', './data/c_neg.txt'
pos_lines = open(pos_f_name).readlines()
neg_lines = open(neg_f_name).readlines()

pos_cut_lines = list(map(lambda x: ' '.join(jieba.cut(x.replace('\n', ''))), pos_lines))
neg_cut_lines = list(map(lambda x: ' '.join(jieba.cut(x.replace('\n', ''))), neg_lines))

for i in pos_cut_lines:
    l1.append(i)

for i in neg_cut_lines:
    l1.append(i)
x = np.array(l1)

# Build vocabulary & sequences
tk = text.Tokenizer(num_words=max_features, split=" ")
tk.fit_on_texts(x)
x = tk.texts_to_sequences(x)
word_index = tk.word_index
x = sequence.pad_sequences(x, maxlen=max_len)

def input_transform(string_list):
    l0 = []
    for ss in string_list:
        string0 = ' '.join(jieba.cut(ss.replace('\n', '')))
        l0.append(string0)
    l0 = np.array(l0)
    input0 = tk.texts_to_sequences(l0)
    input1 = sequence.pad_sequences(input0, maxlen=max_len)
    return input1

def predict(model, string_list):
    input1 = input_transform(string_list)
    result = model.predict(input1)
    return result

def predict_test(string_list):
    result = predict(model, string_list)
    return result

if __name__ == '__main__':
    sent_lines = open('./data/comment.txt').readlines()
    string_list = list(map(lambda x: x.replace('\n', ''), open('./data/comment.txt').readlines()))
    result = predict_test(string_list)
    f_true = open('comparative_true.txt', 'w')
    f_false = open('comparative_false.txt', 'w')
    for i in range(len(result)):
        if result[i][0] > result[i][1]:
            f_true.write(sent_lines[i])
        else:
            f_false.write(sent_lines[i])
