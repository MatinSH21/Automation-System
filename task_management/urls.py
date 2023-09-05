from django.urls import path, include
from task_management import views as task_views

urlpatterns = [
    path('', task_views.TaskListAPIView.as_view(), name='task-list'),
    path('<int:pk>/', task_views.TaskDetailAPIView.as_view(), name='task-detail'),
]
