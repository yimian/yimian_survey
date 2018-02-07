import numpy as np
import random
import jieba
import time

# ======== parameters part start ========
# k_fold value
k_fold = 5

# random seed
rand_seed = 7

# Input parameters
max_features = 50000
max_len = 50
embedding_size = 400
border_mode = 'same'
dropout = 0.5
l2_regularization = 0.2

# RNN parameters
output_size = 50
rnn_activation = 'tanh'
recurrent_activation = 'hard_sigmoid'

# Compile parameters
loss = 'categorical_crossentropy'
optimizer = 'rmsprop'

# Training parameters
batch_size = 128
num_epoch = 50
validation_split = 0
shuffle = True

# build dataset, give each sentence a split number for the cross validation
def build_data_cv(f_pos, f_neg, cv=10):
    """
    Loads the data and split into k folds.
    """
    docs = []
    with open(f_pos, encoding='utf8') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            doc = {
                'y': 1,
                'text': line,
                'split': np.random.randint(0, cv)}
            docs.append(doc)
    with open(f_neg, encoding='utf8') as f:
        for line in f:
            line = line.replace('\n', '')
            doc = {
                'y': 2,
                'text': line,
                'split': np.random.randint(0, cv)
            }
            docs.append(doc)
    return docs

def trans_label_1(i):
    if i == 1:
        return [1, 0]
    if i == 2:
        return [0, 1]

# the main code of lstm train and test, return a final accuracy
def lstm_training_predict(set_traning, label_training, set_test, label_test):
    import gensim
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Activation
    from keras import regularizers
    from keras.layers import Embedding
    from keras.layers import LSTM
    from keras.preprocessing import text, sequence

    # cut sentences to words
    x_training = np.array(list(map(lambda n: ' '.join(jieba.cut(n.replace('\n', ''))), set_traning)))
    y_training = np.array(label_training)
    x_test = np.array(list(map(lambda n: ' '.join(jieba.cut(n.replace('\n', ''))), set_test)))
    y_test = np.array(label_test)

    # Build vocabulary & sequences
    tk = text.Tokenizer(num_words=max_features)
    tk.fit_on_texts(x_training)
    x_training = tk.texts_to_sequences(x_training)
    word_index = tk.word_index
    x_training = sequence.pad_sequences(x_training, maxlen=max_len)

    # Build pre-trained embedding layer
    w2v = gensim.models.Word2Vec.load('movie.model')
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_size))
    for word, i in word_index.items():
        if word in w2v.wv.vocab:
            embedding_matrix[i] = w2v[word]
    embedding_layer = Embedding(len(word_index) + 1, embedding_size, weights=[embedding_matrix], input_length=max_len)
    model = Sequential()
    model.add(embedding_layer)
    model.add(Dropout(dropout))
    model.add(LSTM(output_dim=output_size, activation=rnn_activation, recurrent_activation=recurrent_activation))
    model.add(Dropout(dropout))
    model.add(Dense(2, kernel_regularizer=regularizers.l2(l2_regularization)))
    model.add(Activation('softmax'))
    model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=['accuracy'])
    print('============ LSTM w2v model training begin ===============')
    model.fit(x_training, y_training, batch_size=batch_size, epochs=num_epoch, validation_split=validation_split,
              shuffle=shuffle)
    model.save('compa_sent.model')
    print('============ LSTM w2v model training finish ==============')

    x_test = tk.texts_to_sequences(x_test)
    x_test = sequence.pad_sequences(x_test, maxlen=max_len)
    y_predict = model.predict(x_test)
    y_predict = np.array(list(map(lambda n: n.argmax() + 1, y_predict)))
    pos_true = 0
    neg_true = 0
    pos_pre = 0
    neg_pre = 0
    pos_pre_true = 0
    neg_pre_true = 0
    for i in range(len(y_test)):
        if y_test[i] == 1:
            pos_true += 1
            if y_predict[i] == 1:
                pos_pre_true += 1
        elif y_test[i] == 2:
            neg_true += 1
            if y_predict[i] == 2:
                neg_pre_true += 1
        if y_predict[i] == 1:
            pos_pre += 1
        if y_predict[i] == 2:
            neg_pre += 1
    pos_true_rate = pos_pre_true / pos_pre
    neg_true_rate = neg_pre_true / neg_pre
    pos_recall_rate = pos_pre_true / pos_true
    neg_recall_rate = neg_pre_true / neg_true
    pos_f1 = 2 * pos_true_rate * pos_recall_rate / (pos_true_rate + pos_recall_rate)
    neg_f1 = 2 * neg_true_rate * neg_recall_rate / (neg_true_rate + neg_recall_rate)
    diff = y_predict - y_test
    predict_true = list(filter(lambda n: n == 0, diff))
    accu = len(predict_true) / len(y_predict)

    return pos_true_rate, pos_recall_rate, pos_f1, \
           neg_true_rate, neg_recall_rate, neg_f1, accu



def use_all_to_train(f_pos, f_neg):
    data_cv = build_data_cv(f_pos, f_neg, cv=k_fold)
    random.Random(rand_seed).shuffle(data_cv)  # shuffle
    x_training = []
    y_training = []
    x_test = []
    y_test = []
    set_training = []
    y_test = []
    for doc in data_cv:
        x_training.append(doc['text'])
        y_training.append(doc['y'])
        if doc['split'] == 1:
            x_test.append(doc['text'])
            y_test.append(doc['y'])
    y_training = list(map(trans_label_1, y_training))
    lstm_training_predict(x_training, y_training, x_test, y_test)

# the code of train and test
def train_test(f_pos, f_neg, model_name, pca_flag=False):
    data_cv = build_data_cv(f_pos, f_neg, cv=k_fold)
    random.Random(rand_seed).shuffle(data_cv)  # shuffle
    pos_t_r_list = []
    pos_r_r_list = []
    pos_f_list = []
    neg_t_r_list = []
    neg_r_r_list = []
    neg_f_list = []
    accu_list = []
    if model_name == 'lstm':
        # k fold cross validation in lstm w2v
        for i in range(k_fold):
            print('======== fold %s ========' % i)
            x_training = []
            y_training = []
            x_test = []
            y_test = []
            for doc in data_cv:
                if doc['split'] == i:
                    x_test.append(doc['text'])
                    y_test.append(doc['y'])
                else:
                    x_training.append(doc['text'])
                    y_training.append(doc['y'])
            print("Train/Test split: {:d}/{:d}".format(len(y_training), len(y_test)))
            y_training = list(map(trans_label_1, y_training))
            # train and test
            pos_t_r, pos_r_r, pos_f, neg_t_r, neg_r_r, neg_f, accu = lstm_training_predict(
                x_training, y_training, x_test, y_test)
            pos_t_r_list.append(pos_t_r)
            pos_r_r_list.append(pos_r_r)
            pos_f_list.append(pos_f)
            neg_t_r_list.append(neg_t_r)
            neg_r_r_list.append(neg_r_r)
            neg_f_list.append(neg_f)
            accu_list.append(accu)

        pos_true_rate = sum(pos_t_r_list) / len(pos_t_r_list)
        pos_recall_rate = sum(pos_r_r_list) / len(pos_r_r_list)
        pos_f1 = sum(pos_f_list) / len(pos_f_list)
        neg_true_rate = sum(neg_t_r_list) / len(neg_t_r_list)
        neg_recall_rate = sum(neg_r_r_list) / len(neg_r_r_list)
        neg_f1 = sum(neg_f_list) / len(neg_f_list)
        accu = sum(accu_list) / len(accu_list)

        f_result = open('5_fold_result.txt', 'a')
        local_time = time.strftime("%Y-%m-%d %A %X %Z", time.localtime())
        f_result.write(str(local_time) + '\n')
        f_result.write('model: lstm\n')

        pos_result = 'pos_true_rate: ' + str(pos_true_rate) + '\n' + \
                     'pos_recall_rate: ' + str(pos_recall_rate) + '\n' + \
                     'pos_f1: ' + str(pos_f1) + '\n'

        print(pos_result)
        f_result.write(pos_result)
        neg_result = 'neg_true_rate: ' + str(neg_true_rate) + '\n' + \
                     'neg_recall_rate: ' + str(neg_recall_rate) + '\n' + \
                     'neg_f1: ' + str(neg_f1) + '\n'

        print(neg_result)
        f_result.write(neg_result)
        accu_result = 'accu: ' + str(accu) + '\n'
        print(accu_result)
        f_result.write(accu_result)
        f_result.write('\n\n\n')

if __name__ == '__main__':
    f_pos = './data/c_pos.txt'
    f_neg = './data/c_neg.txt'
    # result_svm = train_test(f_pos, f_neu, f_neg, model_name='svm', pca_flag=True)
    # local_time = time.strftime("%Y-%m-%d %A %X %Z", time.localtime())
    # result_time = result_lstm + str(local_time) + '\n'
    # result_txt = open('result', 'a')
    # result_txt.write(result_time)
    # train_test('./data/ser_pos.txt', './data/ser_neu.txt', './data/ser_neg.txt', model_name='svm', pca_flag=True)
    use_all_to_train(f_pos=f_pos, f_neg=f_neg)
