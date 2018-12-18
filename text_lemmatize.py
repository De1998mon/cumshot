import pymorphy2
import gensim
import logging
import gzip
def read_input(input_file):
    """This method reads the input file which is in gzip format"""

    logging.info("reading file {0}...this may take a while".format(input_file))

    with gzip.open(input_file, 'rb') as f:
        for i, line in enumerate(f):

            if (i % 10000 == 0):
                logging.info("read {0} reviews".format(i))
            # do some pre-processing and return a list of words for each review text
            yield gensim.utils.simple_preprocess(line)

stop_words = ('быть', 'мой', 'наш', 'ваш', 'их', 'его', 'её', 'их',
                  'этот', 'тот', 'где', 'который', 'либо', 'нибудь', 'нет', 'да')
data_file = "out_file.txt.gz"
documents = list(read_input(data_file))
print(documents)
i = 0
k = 0
print(len(documents))
morph = pymorphy2.MorphAnalyzer()
for docs in documents:
    if (i % 1000 == 0):
        print(i, ' ',  k)
    if docs != []:
        j = 0
        for word in docs:
            forms = morph.parse(word)
            form = forms[0]
            if (form.tag.POS in ['NOUN','ADJF', 'ADJS', 'COMP','VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'ADVB', 'PRED']):
                docs[j] = form.normal_form + '_' + form.tag.POS
                j += 1
        documents[i] = docs[:j]
        i += 1
    k += 1
documents = documents[:i]
file = open("res_file_tokenize.txt", "w", encoding="utf-8")
for docs in documents:
    file.write(str(docs))
file.close()