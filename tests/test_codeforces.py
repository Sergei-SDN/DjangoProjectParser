import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from task.models import Task
from task.services import Codeforces


class TestCodeforces(TestCase):

    # Тест для проверки успешного получения данных JSON от API Codeforces
    @patch('requests.get')  # Мокируем метод requests.get
    def test_get_json_from_codeforces_success(self, mock_get):
        # Создаем макетный объект для имитации успешного ответа от API
        mock_response = MagicMock()
        mock_response.content = '{"status": "OK", "result": {"problems": [], "problemStatistics": []}}'
        mock_get.return_value = mock_response  # Задаем возвращаемое значение для мокированного метода

        codeforces = Codeforces()  # Создаем экземпляр класса Codeforces
        response = codeforces.get_json_from_codeforces('https://codeforces.com/api/problemset.problems/')  # Вызываем тестируемый метод

        # Проверяем, что ответ содержит ожидаемый JSON
        self.assertEqual(response.content, '{"status": "OK", "result": {"problems": [], "problemStatistics": []}}')

    # Тест для проверки обработки ошибки соединения при вызове метода get_json_from_codeforces
    @patch('requests.get')  # Мокируем метод requests.get
    def test_get_json_from_codeforces_connection_error(self, mock_get):
        mock_get.side_effect = ConnectionError()  # Задаем исключение, которое будет подниматься при вызове мокированного метода

        codeforces = Codeforces()  # Создаем экземпляр класса Codeforces
        response = codeforces.get_json_from_codeforces('https://codeforces.com/api/problemset.problems/')  # Вызываем тестируемый метод

        # Проверяем, что возвращается пустой словарь в случае ошибки соединения
        self.assertEqual(response, {})

    # Тест для проверки метода get_tasks
    @patch('requests.get')  # Мокируем метод requests.get
    def test_get_tasks(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '{"status": "OK", "result": {"problems": [], "problemStatistics": []}}'
        mock_get.return_value = mock_response  # Задаем возвращаемое значение для мокированного метода

        codeforces = Codeforces()  # Создаем экземпляр класса Codeforces
        tasks = codeforces.get_tasks()  # Вызываем тестируемый метод

        # Проверяем, что список задач пустой
        self.assertEqual(len(tasks), 0)

    # Тест для проверки метода get_task_filter_name
    def test_get_task_filter_name(self):
        task_name = 'test_task'
        Task.objects.create(name=task_name)  # Создаем тестовую задачу в базе данных

        codeforces = Codeforces()  # Создаем экземпляр класса Codeforces
        task_exists = codeforces.get_task_filter_name(name=task_name)  # Вызываем тестируемый метод

        # Проверяем, что задача с указанным именем существует в базе данных
        self.assertTrue(task_exists)

    # Тест для проверки метода add_tasks
    def test_add_tasks(self):
        tasks = [
            Task(name='test_task1', numbers='test1'),
            Task(name='test_task2', numbers='test2')  # Создаем тестовые задачи
        ]

        codeforces = Codeforces()  # Создаем экземпляр класса Codeforces
        codeforces.add_tasks(tasks)  # Вызываем тестируемый метод

        # Проверяем, что задачи успешно добавлены в базу данных
        self.assertEqual(Task.objects.filter(name='test_task1').count(), 1)
        self.assertEqual(Task.objects.filter(name='test_task2').count(), 1)


if __name__ == '__main__':
    unittest.main()

