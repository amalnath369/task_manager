from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskReportView,
    admin_dashboard, task_list, task_detail, user_list, admin_list
)

urlpatterns = [
    # Web interface URLs
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('', task_list, name='task-list'),
    path('<int:task_id>/', task_detail, name='task-detail'),
    path('users/', user_list, name='user-list'),
    path('admins/', admin_list, name='admin-list'),

        # API URLs
    path('api-task', TaskListView.as_view(), name='api-tasks-list'),
    path('api-task/<int:pk>/', TaskDetailView.as_view(), name='api-tasks-detail'),
    path('<int:pk>/report/', TaskReportView.as_view(), name='api-task-report'),

]
