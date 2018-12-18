# lingvo-bot

Команда СЕПУЛЬКИ занималась обучением модели по текстам русской фантастикой.
Данная модель представлена в Telegram боте @lingvo-bot.

С ботом можно взаимодействовать в 4х режимах. Чтобы активировать режим, достаточно написать ключевое слово:
  
  1. "Соседи": после отправки сообщения с данным ключевым словом, бот уведомит Вас об активации режима "Режим ближайших соседей слова" и будет ждать ввода ОДНОГО слова. После чего, бот выдаст 10 ближайших соседей и коэффициент косинусной близости для данного слова.
Напрмиер: солнце

небо 0.776087760925293

солнца 0.7666128873825073
облака 0.7549118995666504
солнышко 0.7541394829750061
солнцу 0.7492870092391968
встающее 0.7396429181098938
луна 0.7342524528503418
небе 0.7322403192520142
синее 0.7273432016372681
светило 0.7258069515228271

  2. "Лишнее": после отправки сообщения с данным ключевым словом, бот уведомит Вас об активации режима "Режим лишнего слова в списке" и будет ждать ввода НЕОГРАНИЧЕННОГО количества слов. После чего, бот выведет лишнее слово из n предложенных.
Например: воробей собака сокол голубь
собака
