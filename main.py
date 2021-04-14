import telebot
import Watson

import libgen

is_parsing = False

NN_TEST_FIRST = 'https://onlinetestpad.com/hpah6ermggsyq'
BOOKS_DISK = 'https://cloud.mail.ru/public/AXg9/rJCvHqD2s'
TELEGRAM_BOT_TOKEN = '1777024279:AAEjnaxv7bZ9MWzZlCyj-MkS6Gu8GhR7QbU'

watson_bot = Watson.Watson()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot_session(message):
    watson_bot.start_session()
    bot.send_message(message.chat.id, "Привет, я бот помощник по ML.")


@bot.message_handler(commands=['stop'])
def start_bot_session(message):
    watson_bot.end_session()
    bot.send_message(message.chat.id, "Диалог окончен.")


# send text from telegram bot  to Watson and send answer into telegram bot
@bot.message_handler(content_types=['text'])
def send_text(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Книги по ML и NN', url=BOOKS_DISK))
    markup.add(telebot.types.InlineKeyboardButton(text='Тесты по Нейронным сетям', url=NN_TEST_FIRST))
    markup.add(telebot.types.InlineKeyboardButton(text='Учебный план', callback_data='plan'))
    markup.add(telebot.types.InlineKeyboardButton(text='Поиск по libgen.com', callback_data='parse'))

    # Если был запрос для парсинга
    global is_parsing
    if is_parsing:
        is_parsing = False
        list_of_books = libgen.search_books(message.text, 3)
        if list_of_books:
            for book in list_of_books:
                bot.send_message(message.chat.id, text=book)
        else:
            bot.send_message(message.chat.id, text="По такому запросу ничего не нашлось.")
        return

    # noinspection PyBroadException
    try:
        response = watson_bot.send(message.text)
        if response == 'materials':
            bot.send_message(message.chat.id, text=f"{BOOKS_DISK}")
        elif response == 'test':
            bot.send_message(message.chat.id, text=f"{NN_TEST_FIRST}")
        elif response == 'curriculum':
            bot.send_photo(message.chat.id, photo=open('Images/image1.jfif', 'rb'))
            bot.send_photo(message.chat.id, photo=open('Images/image2.jfif', 'rb'))
            bot.send_photo(message.chat.id, photo=open('Images/image3.jfif', 'rb'))
        elif response == 'parsing':
            bot.send_message(message.chat.id, text='Введите строку поиска на LibGen:')
            is_parsing = True
        else:
            print('else')
            bot.send_message(message.chat.id, text=response)

    except Exception as e:
        print(e)
        if not watson_bot.session_is_active:
            bot.send_message(message.chat.id, "Напишите /start для запуска бота:")
        else:
            bot.send_message(message.chat.id, text="Можете перефразировать? Или выберите действие:",
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    if call.data == 'parse':
        answer = 'Введите строку поиска на LibGen:'
        global is_parsing
        is_parsing = True
        bot.send_message(call.message.chat.id, answer)
    elif call.data == 'plan':
        bot.send_photo(call.message.chat.id, photo=open('Images/image1.jfif', 'rb'))
        bot.send_photo(call.message.chat.id, photo=open('Images/image2.jfif', 'rb'))
        bot.send_photo(call.message.chat.id, photo=open('Images/image3.jfif', 'rb'))


def main():
    bot.polling()


if __name__ == '__main__':
    main()
