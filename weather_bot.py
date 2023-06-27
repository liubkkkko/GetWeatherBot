import requests
import json     #імпорт необхідних модулів для взаємодії з API та обробки JSON-даних.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters #імпорт необхідних класів для роботи з ботом Telegram.
from telegram import ReplyKeyboardMarkup, KeyboardButton  # імпорт класів для створення клавіатури з кнопками.

#функція, що обробляє команду /start. Відправляє привітальне повідомлення і відображає кнопку для надсилання розташування.
def start(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт! Я бот прогнозу погоди. Натисни кнопку нижче, щоб надіслати мені своє розташування, і я надішлю тобі прогноз погоди на кілька днів!")

#функція, що обробляє текстові повідомлення. Відображає кнопку для надсилання розташування.
def location_button(update, context):
    keyboard = [[KeyboardButton("Надіслати розташування", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Натисни кнопку нижче, щоб надіслати мені своє розташування:", reply_markup=reply_markup)

#функція, що обробляє отримане розташування. Запитує API OpenWeatherMap за допомогою отриманих координат і отримує прогноз погоди на 5 днів. Потім надсилає цей прогноз у вигляді повідомлень.
def location(update, context):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    api_key = '34ab632b43f19bb33c272162e6089d26'  #API-ключ OpenWeatherMap
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)

    forecast_list = data['list'][::8][:5]  # Отримуємо прогноз на 5 днів з інтервалом в 24 години

    for forecast in forecast_list:
        date = forecast['dt_txt']
        temperature = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        message = f"Дата: {date}\nТемпература: {temperature}°C\nОпис: {description}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#функція, що налаштовує бота, додає обробники команд і повідомлень, запускає бота для прослуховування вхідних повідомлень.
def main():
    updater = Updater('5918009023:AAFqB5AAR2E6rQ3epJVLbdB5_gL3J08PlCk', use_context=True)  # токен телеграм-бота
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, location_button))
    dp.add_handler(MessageHandler(Filters.location, location))
#запуск бота для прослуховування вхідних повідомлень.
    updater.start_polling()
#зупинка бота після натискання Ctrl+C або отримання сигналу зупинки.
    updater.idle()

if __name__ == '__main__':
    main()


