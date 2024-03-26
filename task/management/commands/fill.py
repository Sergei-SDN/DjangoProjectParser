from django.core.management.base import BaseCommand

from task.services import Codeforces


# Определение пользовательской команды для управления ботом
class Command(BaseCommand):

    # Основной метод, который будет вызываться при выполнении команды
    def handle(self, *args, **options):
        # Создание нового объекта подключения к Codeforces
        new_conn = Codeforces()
        # Получение задач с использованием API Codeforces
        tasks = new_conn.get_tasks()
