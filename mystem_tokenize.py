#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from __future__ import division
from future import standard_library
import sys
import requests
from pymystem3 import Mystem
from many_stop_words import get_stop_words
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

'''
Этот скрипт принимает на вход необработанный русский текст (одно предложение на строку или один абзац на строку).
Он токенизируется, лемматизируется и размечается по частям речи с использованием Mystem.
На выход подаётся последовательность разделенных пробелами лемм с частями речи ("зеленый_NOUN трамвай_NOUN").
Их можно непосредственно использовать в моделях с RusVectōrēs (http://rusvectores.org).
Примеры запуска:
echo 'Мама мыла раму.' | python3 rus_preprocessing_mystem.py
zcat large_corpus.txt.gz | python3 rus_preprocessing_mystem.py | gzip > processed_corpus.txt.gz
'''


def tag_mystem(text='Текст нужно передать функции в виде строки!', mapping=None, postags=True):
    # если частеречные тэги не нужны (например, их нет в модели), выставьте postags=False
    # в этом случае на выход будут поданы только леммы

    processed = m.analyze(text)
    tagged = []
    for w in processed:
        try:
            lemma = w["analysis"][0]["lex"].lower().strip()
            pos = w["analysis"][0]["gr"].split(',')[0]
            pos = pos.split('=')[0].strip()
            if mapping:
                if pos in mapping:
                    pos = mapping[pos]  # здесь мы конвертируем тэги
                else:
                    pos = 'X'  # на случай, если попадется тэг, которого нет в маппинге
            tagged.append(lemma.lower() + '_' + pos)
        except KeyError:
            continue  # я здесь пропускаю знаки препинания, но вы можете поступить по-другому
        except IndexError:
            continue
    if not postags:
        tagged = [t.split('_')[0] for t in tagged]
    return tagged


standard_library.install_aliases()

# Таблица преобразования частеречных тэгов Mystem в тэги UPoS:
mapping_url = \
    'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

mystem2upos = {}
r = requests.get(mapping_url, stream=True)
for pair in r.text.split('\n'):
    pair = pair.split()
    if len(pair) > 1:
        mystem2upos[pair[0]] = pair[1]

print('Loading the model...', file=sys.stderr)
m = Mystem()


# создаёт из текста список вида 'слово_частьречи'
textfile = '/Users/ln/Documents/PyCharm/texts/all2.txt'
text = open(textfile, 'r', encoding='utf-8').read()
output = tag_mystem(text=text, mapping=mystem2upos)
print(len(output))
print(' '.join(output))


# удаляет стоп слова (предлоги, местоимения и служебные части речи)
# list вида: 'слово_частьречи'
# Напрмиер: 'ягупов_NOUN', 'а_SCONJ', 'вы_PRON', 'не_PART', 'верить_VERB'
def delete_stop_words_from_list(l):
    stop_words = list(get_stop_words('ru'))  # About 900 stopwords
    nltk_words = list(stopwords.words('russian'))  # About 150 stopwords
    stop_words.extend(nltk_words)
    out = []
    for x in l:
        if x[: x.find('_')] in stop_words:
            continue
        else:
            out.append(x)
    return out


# засовываем всё в один файл
f = open('final without stop words.txt', 'w')
out = delete_stop_words_from_list(output)
print(out)
f.write(str(out))
f.close()
