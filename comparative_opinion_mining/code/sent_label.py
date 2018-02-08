import jieba

def read_corpus_to_dict():
    car_sent = open('./data/car_sent.txt', encoding='utf8').readlines()
    car_term = open('./data/car_term.txt', encoding='utf8').readlines()
    car_dict = {}
    # digital_sent = open('./data/digital_sent.txt', encoding='utf8').readlines()
    # digital_term = open('./data/digital_term.txt', encoding='utf8').readlines()
    # digital_dict = {}
    for line in car_sent:
        parts = line.split('\t')
        if parts[2].replace('\n', '') == '1':
            car_dict[parts[0]] = {}
            car_dict[parts[0]]['sent'] = parts[1]
            car_dict[parts[0]]['terms'] = []
            car_dict[parts[0]]['aspects'] = []
    for line in car_term:
        parts = line.split('\t')
        if parts[3] != 'NULL':
            if parts[3] not in car_dict[parts[1]]['terms']:
                car_dict[parts[1]]['terms'].append(parts[3])
        if parts[4] != 'NULL':
            if parts[4] not in car_dict[parts[1]]['aspects']:
                car_dict[parts[1]]['aspects'].append(parts[4])
    return car_dict

def select_cut(sent, l_1, l_2):
    if sent not in l_1 and sent not in l_2:
        return list(jieba.cut(sent))
    else:
        return sent

if __name__ == '__main__':
    car_dict = read_corpus_to_dict()
    print(car_dict['DOC16'])
    f_label = open('car_label.txt', 'w', encoding='utf8')
    for i in car_dict.items():
        sent = i[1]['sent']
        terms = i[1]['terms']
        aspects = i[1]['aspects']
        # print(i[1]['sent'])
        # print(terms)
        # print(aspects)
        for i in terms:
            sent = sent.replace(i, ' ' + i + ' ')
        for i in aspects:
            sent = sent.replace(i, ' ' + i + ' ')
        print(sent)
        sent_list = sent.split(' ')
        new_sent_list = []
        for i in sent_list:
            if i not in terms and i not in aspects:
                i = list(jieba.cut(i))
                i = list(map(lambda x: x + '/o', i))
                part = ' '.join(i)
                new_sent_list.append(part)
            elif i in terms:
                new_sent_list.append(i + '/t')
            else:
                new_sent_list.append(i + '/a')
        f_label.write(' '.join(new_sent_list) + '\n')
            