import json
import os
from abc import ABC, abstractmethod

import django
import requests

from task.models import Task


# Определение абстрактного базового класса для работы с API
class API(ABC):

    @abstractmethod
    def get_tasks(self):
        pass


# Класс для работы с API Codeforces, наследуется от абстрактного класса API
class Codeforces(API):

    def __init__(self):
        # Установка переменных окружения для настроек Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.settings')
        # Инициализация Django
        django.setup()
        # Имя соединения
        self.name = 'codeforces_conn'
        # URL API Codeforces для получения задач
        self.url = 'https://codeforces.com/api/problemset.problems/'

    def __repr__(self):
        # Представление объекта в виде строки для отладки
        return f"{self.__class__.__name__} {self.name}"

    def __str__(self):
        # Строковое представление объекта
        return f"{self.name}"

    def get_tasks(self, query=''):

        """Парсинг задач с сайта CODEFORCES"""

        new_tasks_list = []
        # Получение данных в формате JSON с API Codeforces
        request = self.get_json_from_codeforces(self.url + query)
        parsed = json.loads(request.content)
        request.close()

        # Проверка статуса ответа API
        if parsed.get('status') == "OK":
            # Получение данных о задачах
            tasks_data = parsed['result']['problems']
            # Получение данных о статистике решений задач
            solutions = parsed['result']['problemStatistics']
            for task in tasks_data:
                if task:
                    # Фильтрация данных для получения количества решений конкретной задачи
                    filtering = list(
                        filter(lambda x: (task['contestId'] == x.get('contestId')) and task['index'] == x.get('index'),
                               solutions))
                    if filtering:
                        solved = filtering[0].get('solvedCount')

                    # Проверка наличия задачи в базе данных
                    task_exists = task is not None and self.get_task_filter_name(name=task.get('name'))
                    if task_exists:
                        continue

                    # Создание объектов задач для добавления в базу данных
                    new_tasks_list.append(
                        Task(
                            name=task['name'],
                            tags=task['tags'],
                            complexity=task.get('rating') if task.get('rating') is not None else 0,
                            numbers=str(task.get('contestId')) + task.get('index'),
                            count_solutions=solved if solved is not None else 0,
                            index=task.get('index'),
                            number_contest=task.get('contestId')
                        )
                    )

            # Добавление новых задач в базу данных
            self.add_tasks(new_tasks_list)
        return new_tasks_list

    def get_json_from_codeforces(self, query=''):
        # Отправка запроса к API Codeforces и обработка исключений
        try:
            response = requests.get(query)
            return response
        except ConnectionError:
            print('Connection Error')
        except requests.HTTPError:
            print('HTTP error')
        except TimeoutError:
            print('Timeout Error')
        return {}

    def get_task_filter_name(self, name):
        # Проверка существования задачи с указанным именем в базе данных
        return Task.objects.filter(name=name).exists()

    def add_tasks(self, tasks):
        # Массовое добавление задач в базу данных
        Task.objects.bulk_create(tasks)


# Функция для фильтрации задач по сложности
def get_task_filter_complexity(filter):
    return list(Task.objects.filter(complexity=filter))


# Функция для фильтрации задач по тегам
def get_task_filter_tags(filter):
    return list(Task.objects.filter(tags__icontains=filter))
