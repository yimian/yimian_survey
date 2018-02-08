# 所有词语
ww = []
# 所有的词性
pos = []
# 每个词性出现的频率
fre = {}
# 先验概率矩阵
pi = {}
# 状态转移概率矩阵
A = {}
# 观测概率矩阵
B = {}
# dp概率
dp = []
# 路径记录
pre = []
zz = {}

train_lines = open('car_label.txt', encoding='utf8').readlines()

for line in train_lines:
    tmp = line.replace('\n', '').split(' ')
    n = len(tmp)
    for i in range(n):
        word_tag = tmp[i].split('/')
        if word_tag[0] not in ww:
            ww.append(word_tag[0])
            if word_tag[1] not in pos:
                pos.append(word_tag[1])
print(pos)
print(ww[:3])
print('奔驰' in ww)
print('宝马' in ww)
print('设计' in ww)

for i in pos:
    pi[i] = 0
    fre[i] = 0
    A[i] = {}
    B[i] = {}
    for j in pos:
        A[i][j] = 0
    for j in ww:
        B[i][j] = 0

line_num = 0
for line in train_lines:
    line_num += 1
    tmp = line.replace('\n', '').split(' ')
    n = len(tmp)
    for i in range(0, n):
        word_tag = tmp[i].split('/')
        word_tag_pre = tmp[i - 1].split('/')
        fre[word_tag[1]] += 1
        if (i == 1):
            pi[word_tag[1]] += 1
        elif i > 0:
            A[word_tag_pre[1]][word_tag[1]] += 1
        B[word_tag[1]][word_tag[0]] += 1

cx = {}
cy = {}

for i in pos:
    cx[i] = 0
    cy[i] = 0
    pi[i] = pi[i] * 1.0 / line_num
    for j in pos:
        if(A[i][j] == 0):
            cx[i] += 1
            A[i][j] = 0.5
    for j in ww:
        if(B[i][j] == 0):
            cy[i] += 1
            B[i][j] = 0.5

for i in pos:
    pi[i] = pi[i] * 1.0 / line_num
    for j in pos:
        A[i][j] = A[i][j] * 1.0 / (fre[i] + cx[i])
    for j in ww:
        B[i][j] = B[i][j] * 1.0 / (fre[i] + cy[i])

print(cx)
print(cy)
print(A)

def get_sent_tag(sent):
    items = sent.split(' ')
    words = []
    tags = []
    for i in items:
        words.append(i.split('/')[0])
        tags.append(i.split('/')[1])
    word_str = ' '.join(words)
    tag_str = ' '.join(tags)
    return word_str, tag_str


def vetebi_decode(input_sent):
    tmp = input_sent
    text = tmp.split(' ')
    num = len(text)
    dp = [{} for i in range(num)]
    pre = [{} for i in range(num)]

    for k in pos:
        for j in range(num):
            dp[j][k] = 0
            pre[j][k] = ''

    n = len(pos)
    for c in pos:
        if(text[0] in B[c]):
            dp[0][c] = pi[c] * B[c][text[0]] * 1000
        else:
            dp[0][c] = pi[c] * 0.5 * 1000 / (cy[c] + fre[c])

    for i in range(1, num):
        for j in pos:
            for k in pos:
                tt = 0
                if(text[i] in B[j]):
                    tt = B[j][text[i]] * 1000
                else:
                    tt = 0.5 * 1000 / (cy[j] + fre[j])
                if(dp[i][j] < dp[i - 1][k] * A[k][j] * tt):
                    dp[i][j] = dp[i - 1][k] * A[k][j] * tt
                    pre[i][j] = k
    res = {}
    tag_list = []
    MAX = ""
    for j in pos:
        if(MAX == "" or dp[num - 1][j] > dp[num - 1][MAX]):
            MAX = j
    if(dp[num - 1][MAX] == 0):
        print('error')
    i = num - 1
    while(i >= 0):
        res[i] = MAX
        MAX = pre[i][MAX]
        i -= 1
    for i in range(0, num):
        # print(text[i] + "\\" + res[i])
        tag_list.append(res[i])
    return tag_list


sent_1 = '凯越 太 难看'
sent_2 = '在/o 做工/a 上/o ：/o 吉利/t 不如/o 夏利/t 。/o'
sent_3 = '奔驰 的 设计 比 宝马 好看'

sent_test, tag_test = get_sent_tag(sent_2)
print(sent_test)
print(tag_test)
vetebi_decode(sent_3)

# test the result in training data
a_tag_num = 0
t_tag_num = 0
o_tag_num = 0

a_predict_num = 0
t_predict_num = 0
o_predict_num = 0

a_predict_true = 0
t_predict_true = 0
o_predict_true = 0

true_num_line = 0

for line in train_lines:
    line = line.replace('\n', '')
    items = line.split(' ')
    words = []
    test_tags = []
    for i in items:
        words.append(i.split('/')[0])
        test_tags.append(i.split('/')[1])
    word_str = ' '.join(words)
    # print(word_str)
    # print(vetebi_decode(word_str))
    predict_tags = vetebi_decode(word_str)
    
    if predict_tags == test_tags:
        true_num_line += 1
    

    # stastics the a t o tag num
    for tag in test_tags:
        if tag == 'a':
            a_tag_num += 1
        elif tag == 't':
            t_tag_num += 1
        elif tag == 'o':
            o_tag_num += 1

    for i in range(len(test_tags)):
        test_tag = test_tags[i]
        predict_tag = predict_tags[i]
        if predict_tag == 'a':
            a_predict_num += 1
            if test_tag == 'a':
                a_predict_true += 1
        if predict_tag == 't':
            t_predict_num += 1
            if test_tag == 't':
                t_predict_true += 1
        if predict_tag == 'o':
            o_predict_num += 1
            if test_tag == 'o':
                o_predict_true += 1
    

print('a_tag_num', a_tag_num)
print('t_tag_num', t_tag_num)
print('o_tag_num', o_tag_num)

print('a_predict_num', a_predict_num)
print('t_predict_num', t_predict_num)
print('o_predict_num', o_predict_num)

print('a_predict_true', a_predict_true)
print('t_predict_true', t_predict_true)
print('o_predict_true', o_predict_true)

a_precision = a_predict_true / a_predict_num
a_recall = a_predict_true / a_tag_num

t_precision = t_predict_true / t_predict_num
t_recall = t_predict_true / t_tag_num

o_precision = o_predict_true / o_predict_num
o_recall = o_predict_true / o_tag_num

print('a_precision', a_precision)
print('a_recall', a_recall)

print('t_precision', t_precision)
print('t_recall', t_recall)

print('o_precision', o_precision)
print('o_recall', o_recall)

# result of 1000
# a_tag_num 1071
# t_tag_num 2062
# o_tag_num 19897

# a_predict_num 119
# t_predict_num 1154
# o_predict_num 21757

# a_predict_true 110
# t_predict_true 1090
# o_predict_true 19824

# a_precision 0.9243697478991597
# a_recall 0.10270774976657329
# t_precision 0.9445407279029463
# t_recall 0.5286129970902037
# o_precision 0.9111550305648757
# o_recall 0.9963311051917374

# result of 800
# a_tag_num 853
# t_tag_num 1663
# o_tag_num 16075
# a_predict_num 74
# t_predict_num 885
# o_predict_num 17632
# a_predict_true 70
# t_predict_true 838
# o_predict_true 16024
# a_precision 0.9459459459459459
# a_recall 0.08206330597889801
# t_precision 0.9468926553672317
# t_recall 0.5039085989176187
# o_precision 0.9088021778584392
# o_recall 0.9968273716951789

# result of 500
# a_tag_num 509
# t_tag_num 1004
# o_tag_num 9899
# a_predict_num 41
# t_predict_num 463
# o_predict_num 10908
# a_predict_true 39
# t_predict_true 448
# o_predict_true 9882
# a_precision 0.9512195121951219
# a_recall 0.07662082514734773
# t_precision 0.9676025917926566
# t_recall 0.44621513944223107
# o_precision 0.905940594059406
# o_recall 0.9982826548136176

print(true_num_line)