from django.contrib import admin
from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'tags',
                    'count_solutions',
                    'name',
                    'numbers',
                    'index',
                    'complexity',
                    'number_contest',
                    )

