from gensim.models import Word2Vec


model = Word2Vec.load('word2vec10.model')
words = ['искатель_NOUN', 'ночь_NOUN', 'человек_NOUN', 'возбудить_VERB', 'студент_NOUN', 'эльф_NOUN', 'мальчик_NOUN', 'меч_NOUN', 'книга_NOUN']
for word in words:
    # есть ли слово в модели? Может быть, и нет
    if word in model:
        print(word)
        # выдаем 10 ближайших соседей слова:
        for i in model.most_similar(positive=[word], topn=10):
            # слово + коэффициент косинусной близости
            print(i[0], i[1])
        print('\n')
    else:
        # Увы!
        print(word + ' is not present in the model')
print(model.similarity(w1="ночь_NOUN", w2="день_NOUN"))