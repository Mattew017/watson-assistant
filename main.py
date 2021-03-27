import telebot
import Watson

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


# send text from telegram bot  to Watson and send ansert into telegram bot
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        response = watson_bot.send(message.text)
    except Exception as e:
        print(e)
    try:
        bot.send_message(message.chat.id, response)
    except Exception as e:
        print(response)
        print(e)
        if not watson_bot.session_is_active:
            bot.send_message(message.chat.id, "Напишите /start для запуска бота:")
        else:
            bot.send_message(message.chat.id, "Я вас не понял, можете перефразировать?")


def main():
    bot.polling()


if __name__ == '__main__':
    main()
