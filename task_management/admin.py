from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'created_date', 'due_date', 'author', 'status']
    list_filter = ['status', 'priority', ]
    search_fields = ['title', 'description']
