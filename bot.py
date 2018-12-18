import sys
import telebot
import gensim, logging

model = gensim.models.Word2Vec.load('word2vec7.model')
model.init_sims(replace=True)

TOKEN = '708437164:AAFGnigA8oA0ccsUPzFNGNWkAi4kbPE-hDU'

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=["text"])
# Глобальная переменная, которая хранит текущий режим работы
request_type=''

def answer(message):
    global request_type
    if message.text.lower() == 'соседи':
        request_type = 'similar words'
        bot.send_message(message.chat.id, 'Режим ближайших соседей слова')
    elif message.text.lower() == 'лишнее':
        request_type = 'irrelevant word'
        bot.send_message(message.chat.id, 'Режим лишнего слова в списке')
    elif message.text.lower() == 'похожесть':
        request_type = 'similarity'
        bot.send_message(message.chat.id, 'Режим схожести двух слов')
    # добваить похожесть elif
    else:
        words = message.text.lower().split()
        if request_type == '':
            bot.send_message(message.chat.id, 'Задайте режим запросов.')
        # Если режим ближайших соседей слова
        elif request_type == 'similar words':
            msg = ''
            if len(words) != 1:
                bot.send_message(message.chat.id, 'Введите одно слово!')
            elif words[0] not in model:
                bot.send_message(message.chat.id, 'Слово ' + str(words[0]) + 'отсутствует в модели :(')
            else:
                msg += word + '\n'
                # выдаем 10 ближайших соседей слова:
                for i in model.wv.most_similar(positive=[words[0]], topn=10):
                    # слово + коэффициент косинусной близости
                    msg += str(i[0]) + ' ' + str(i[1]) + '\n'
                bot.send_message(message.chat.id, msg)
        # Если режим лишнего слова в списке
        elif request_type == 'irrelevant word':
            if len(words) < 2:
                bot.send_message(message.chat.id, 'Введено слишком мало слов. Попробуйте снова.')
            else:
                doesnt_exist = -1
                for i in range(len(words)):
                    if words[i] not in model:
                        doesnt_exist = i
                        break
                if doesnt_exist == -1:
                    bot.send_message(message.chat.id, model.doesnt_match(words))
                else:
                    bot.send_message(message.chat.id, 'Слово ' + str(words[i]) + 'отсутствует в модели :(')
        # Если режим лишнего слова в списке
        elif request_type == 'similarity':
            if len(words != 2):
                 bot.send_message(message.chat.id, 'Ошибка! Введите два слова!')
            elif words[0] not in model:
                bot.send_message(message.chat.id, 'Слово ' + str(words[0]) + 'отсутствует в модели :(')
            elif words[1] not in model:
                bot.send_message(message.chat.id, 'Слово ' + str(words[1]) + 'отсутствует в модели :(')
            else: 
                bot.send_message(message.chat.id, str(model.similarity(words[0], words[1])))
                
if __name__ == '__main__':
    bot.polling(none_stop=True)
