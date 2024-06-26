from bs4 import BeautifulSoup
import telebot
import requests
import datetime
import time


class Bot:
    def __init__(self):
        self.TOKEN = "TOKEN"
        self.bot = telebot.TeleBot(self.TOKEN)
        self.month = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
                 7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}

        @self.bot.message_handler(commands=["help", "start"])
        def send_message(message):
            self.bot.send_message(message.chat.id, "Я Календарь-бот, отправь мне ссылку для экспорта событий из Яндекс.Календаря в формате HTML")

        @self.bot.message_handler(content_types=['text'])
        def echo_message(message):
            if message.text[:38] == "https://calendar.yandex.ru/export/html":
                self.HTML = message.text
                self.id = message.chat.id
                self.bot.send_message(message.chat.id, "Работаю!")
                while True:
                    self.message_events()
                    time.sleep(1)
            else:
                self.bot.send_message(message.chat.id, "Это явно не ссылка")

    def run(self):
        self.bot.infinity_polling()

    # Проверка на наличие событий на сегодняшний день (Парсинг и добавление в словарь)
    def response(self):
        response = requests.get(self.HTML)
        soup = BeautifulSoup(response.text, features='html.parser')
        tag_div = soup.find_all('div', attrs={'class': 'b-content-event'})
        self.events = {}
        for tag_a in tag_div:
            date = tag_a.find("span").text.split()
            if int(date[0]) == datetime.date.today().day \
                    and date[1] == self.month[datetime.date.today().month]:
                self.events[tag_a.find("span").text] = tag_a.find("h1").text

    # Отправка сообщений в чат
    def message_events(self):
        self.response()
        for event in self.events:
            if str(datetime.datetime.now()).split()[1][:5] == str(event).split()[-1]:
                self.bot.send_message(self.id, f"Событие: {self.events[event]}")
                time.sleep(60)


bot = Bot()
