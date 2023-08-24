from django.db import models
from django.utils.translation import gettext_lazy as _
from user_management.models import Employee


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    author = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True, null=True)
    assigned_to = models.ManyToManyField(Employee, blank=True, null=True, related_name='assigned_tasks')
    due_date = models.DateField(_('due date'), blank=True, null=True)
    priority = models.CharField(_('priority'), max_length=7, choices=PRIORITY_CHOICES, blank=True)
    status = models.CharField(_('status'), max_length=15, choices=STATUS_CHOICES, blank=True, default='todo')
    is_active = models.BooleanField(_('is active'), default=False)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_date = models.DateTimeField(_('updated date'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_management_task'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
