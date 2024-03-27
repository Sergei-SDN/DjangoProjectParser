from django.test import TestCase
from .models import Task


class TaskTestCase(TestCase):

    def setUp(self):
        Task.objects.create(
            name="Diamond Theft",
            tags=['bitmasks', 'dp', 'greedy', 'math', 'sortings', 'two pointers'],
            count_solutions=502,
            numbers="1886E",
            index="E",
            complexity="1000",
            number_contest='1886'
        )

    def test_task_creation(self):
        diamond_theft = Task.objects.get(name="Diamond Theft")
        expected_tags = ['bitmasks', 'dp', 'greedy', 'math', 'sortings', 'two pointers']
        # Преобразуем строку в список
        actual_tags = eval(diamond_theft.tags)
        self.assertEqual(actual_tags, expected_tags)
        self.assertEqual(diamond_theft.name, "Diamond Theft")
        self.assertEqual(diamond_theft.count_solutions, 502)
        self.assertEqual(diamond_theft.numbers, "1886E")
        self.assertEqual(diamond_theft.index, "E")
        self.assertEqual(diamond_theft.complexity, "1000")
        self.assertEqual(diamond_theft.number_contest, '1886')
