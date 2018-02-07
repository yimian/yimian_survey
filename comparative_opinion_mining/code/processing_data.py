from parsel import Selector
import os

def split_docs():
    with open('./lines_39554.txt', 'r') as f:
        content = f.read()

    food_pos = open('food_pos.txt', 'w')
    food_neu = open('food_neu.txt', 'w')
    food_neg = open('food_neg.txt', 'w')

    price_pos = open('price_pos.txt', 'w')
    price_neu = open('price_neu.txt', 'w')
    price_neg = open('price_neg.txt', 'w')

    env_pos = open('env_pos.txt', 'w')
    env_neu = open('env_neu.txt', 'w')
    env_neg = open('env_neg.txt', 'w')

    ser_pos = open('ser_pos.txt', 'w')
    ser_neu = open('ser_neu.txt', 'w')
    ser_neg = open('ser_neg.txt', 'w')

    # build the htmlXPathSelector
    hxs = Selector(text=content)
    docs = hxs.xpath('//sentence').extract()
    i = 0
    for doc in docs:
        i += 1
        hxs0 = Selector(text=doc)
        text = hxs0.xpath('/html/body/sentence/text/text()').extract_first()
        cate = hxs0.xpath('//aspectcategory/@category').extract()
        pola = hxs0.xpath('//aspectcategory/@polarity').extract()
        if 'food' in cate:
            if pola[cate.index('food')] == '1':
                food_pos.write(text + '\n')
            elif pola[cate.index('food')] == '2':
                food_neu.write(text + '\n')
            elif pola[cate.index('food')] == '3':
                food_neg.write(text + '\n')

        if 'price' in cate:
            if pola[cate.index('price')] == '1':
                price_pos.write(text + '\n')
            elif pola[cate.index('price')] == '2':
                price_neu.write(text + '\n')
            elif pola[cate.index('price')] == '3':
                price_neg.write(text + '\n')

        if 'environment' in cate:
            if pola[cate.index('environment')] == '1':
                env_pos.write(text + '\n')
            elif pola[cate.index('environment')] == '2':
                env_neu.write(text + '\n')
            elif pola[cate.index('environment')] == '3':
                env_neg.write(text + '\n')

        if 'service' in cate:
            if pola[cate.index('service')] == '1':
                ser_pos.write(text + '\n')
            elif pola[cate.index('service')] == '2':
                ser_neu.write(text + '\n')
            elif pola[cate.index('service')] == '3':
                ser_neg.write(text + '\n')
    print(i)


def tran_xml():
    f = open('dianping.txt')
    clean_f = open('label_category_dianping11.txt', 'w')
    dict_list = []
    lines = f.readlines()
    for i in range(len(lines)):
        if lines[i] == '<DOC>\n':
            dict1 = {}
            category = lines[i + 1]
            content = lines[i + 2]
            dict1['category'] = category.replace('\n', '')
            dict1['content'] = content.replace('\n', '')
            dict_list.append(dict1)
    print(len(dict_list))
    semeval_tmp = '<sentence>\n' \
                  '\t<rating>%s</rating>\n' \
                  '\t<text>%s</text>\n' \
                  '\t<aspectCategories>\n' \
                  '\t\t<aspectCategory category="food" polarity="1"/>\n' \
                  '\t\t<aspectCategory category="price" polarity="1"/>\n' \
                  '\t\t<aspectCategory category="environment" polarity="1"/>\n' \
                  '\t\t<aspectCategory category="service" polarity="1"/>\n' \
                  '\t</aspectCategories>\n' \
                  '</sentence>'

    for i in range(10000):
        clean_f.write(semeval_tmp%(dict_list[i]['category'], dict_list[i]['content']) + '\n')


def get_lines(line_num):
    f = open('label_v7.txt')
    f1 = open('lines_%s.txt'%line_num, 'w')
    for i in range(line_num):
        line = f.readline()
        f1.write(line)


def proccess_laptops():
    all_terms = []
    with open('./Laptops_Train.xml') as f:
        content = f.read()
    hxs = Selector(text=content)
    docs = hxs.xpath('//sentence').extract()
    for doc in docs:
        hxs0 = Selector(text=doc)
        terms = hxs0.xpath('//aspectterm/@term').extract()
        for term in terms:
            if term not in all_terms:
                all_terms.append(term)
    return all_terms

def stastic_lines():
    f_list = os.listdir('./data/dc/')
    for f_name in f_list:
        print(f_name)
        with open('./data/dc/'+f_name, 'r', encoding='utf-8') as f:
            line_num = len(f.readlines())
            print(line_num)


if __name__ == '__main__':
    #all_term = proccess_laptops()
    stastic_lines()
