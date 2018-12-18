
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import logging


def read_tokenize(text):
    res = []
    i = 0
    text = text.lstrip('[')
    text = text.rstrip(']')
    for sentences in text.split(']['):
        sentences = sentences.strip('\'')
        res.append(sentences.split('\', \''))
    return res



file = open("res_file_tokenize.txt", "r", encoding="utf-8")
text = file.read()
documents = read_tokenize(text)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
path = get_tmpfile("word2vec10.model")
model = Word2Vec(documents, size=200, window=5, min_count=3, workers=6)
model.train(documents, total_examples=len(documents), epochs=20)
model.save("word2vec10.model")



