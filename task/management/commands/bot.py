import os
import django
import random
import time

from django.conf import settings
from django.core.management import BaseCommand
from telebot import TeleBot

from task.services import get_task_filter_complexity, get_task_filter_tags

# Установка переменных окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.settings')
# Инициализация Django
django.setup()

# Инициализация бота с использованием API-ключа из настроек Django
bot = TeleBot(settings.TELEGRAM_API, threaded=False)


# Определение пользовательской команды для управления ботом
class Command(BaseCommand):
    # Краткое описание команды
    help = 'Just a command for launching a Telegram bot'

    # Основной метод, который будет вызываться при выполнении команды
    def handle(self, *args, **kwargs):
        # Включение сохранения следующих шагов обработчиков с задержкой 2 секунды
        bot.enable_save_next_step_handlers(delay=2)
        # Загрузка ранее сохраненных обработчиков шагов
        bot.load_next_step_handlers()

        # Обработчик команды /start
        @bot.message_handler(commands=['start'])
        def start(message):
            # Приветственное сообщение с использованием имени и фамилии пользователя
            mess = (f'Привет, <b>{message.from_user.first_name}</b> <u>{message.from_user.last_name}</u>! \n'
                    f'Этот супер бот поможет выбрать тебе задачи с сайта CODEFORCES\n'
                    f'Введите сложность задачи и тему\n'
                    f'Например: 1000 math'
                    )
            # Отправка приветственного сообщения пользователю
            bot.send_message(message.chat.id, mess, parse_mode='html')

        # Обработчик текстовых сообщений
        @bot.message_handler()
        def get_user_text(message):
            # Список для хранения задач
            task_list = []
            # Список для хранения результата
            result = []

            # Разделение текста сообщения на элементы
            text = message.text.split()

            # Проверка наличия текста
            if text:
                # Итерация по элементам текста
                for item_filter in text:
                    # Если элемент является числом, фильтрация задач по сложности
                    if item_filter.isdigit():
                        complex = get_task_filter_complexity(item_filter)
                        task_list.extend(complex)
                    # Иначе фильтрация задач по тегу
                    else:
                        tag = get_task_filter_tags(item_filter)
                        task_list.extend(tag)

            # Проверка наличия задач в списке
            if task_list:
                # Итерация по задачам и добавление в результат
                for item_task in task_list:
                    result.append(item_task.name + " " + item_task.numbers)

            # Если результат пуст, сообщение об отсутствии задач
            if not result:
                answer = "Нет задач с необходимой темой и сложностью"
            # Иначе выбор случайных 10 задач и формирование ответа
            else:
                finish = random.sample(result, 10)
                answer = ", ".join(finish)
            # Отправка ответа пользователю
            bot.send_message(message.chat.id, answer)

        # Бесконечный цикл работы бота
        while True:
            try:
                # Запуск бота
                bot.polling(none_stop=True)
            except Exception as e:
                # Вывод сообщения об ошибке и пауза перед повторной попыткой
                print('Ошибка:', e)
                time.sleep(5)
