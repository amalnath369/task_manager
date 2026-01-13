from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskCompletionSerializer, TaskReportSerializer
from users.models import User
from utils.permissions import (
    IsAdmin, IsUser, IsTaskOwner, 
    IsAdminOrTaskOwner, IsSuperAdmin
)


# API Views
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'USER':
            return Task.objects.filter(assigned_to=user)
        elif user.role == 'ADMIN':
            return Task.objects.filter(
                assigned_to__admin=user
            ) | Task.objects.filter(assigned_by=user)
        elif user.role == 'SUPERADMIN':
            return Task.objects.all()
        return Task.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'USER':
            raise PermissionDenied("Users cannot create tasks")
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrTaskOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'USER':
            return Task.objects.filter(assigned_to=user)
        elif user.role == 'ADMIN':
            return Task.objects.filter(assigned_to__admin=user) | Task.objects.filter(assigned_by=user)
        elif user.role == 'SUPERADMIN':
            return Task.objects.all()
        return Task.objects.none()
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        
        if request.user.role == 'USER' and task.assigned_to != request.user:
            raise PermissionDenied("You can only update your own tasks")
        
        if request.user.role == 'USER':
            allowed_fields = ['status', 'completion_report', 'worked_hours']
            for field in request.data:
                if field not in allowed_fields:
                    return Response(
                        {'error': f'Users can only update: {", ".join(allowed_fields)}'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            if request.data.get('status') == 'COMPLETED':
                if not request.data.get('completion_report'):
                    return Response(
                        {'completion_report': 'Completion report is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if not request.data.get('worked_hours'):
                    return Response(
                        {'worked_hours': 'Worked hours are required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        return super().update(request, *args, **kwargs)


class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        return Task.objects.filter(status='COMPLETED')
    
    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        if not task.can_view_report(request.user):
            return Response(
                {'error': 'You do not have permission to view this report'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(task)
        return Response(serializer.data)


# Web Interface Views
@login_required
def admin_dashboard(request):
    if not (request.user.is_superadmin or request.user.is_admin):
        return redirect('/tasks/')
    
    context = {
        'user': request.user,
    }
    return render(request, 'tasks/panel_dashboard.html', context)

@login_required
def task_list(request):
    if request.user.is_superadmin:
        tasks = Task.objects.all()
    elif request.user.is_admin:
        # Admin sees tasks of their users and tasks they created
        tasks = Task.objects.filter(
            assigned_to__admin=request.user
        ) | Task.objects.filter(assigned_by=request.user)
    else:
        # Regular user
        tasks = Task.objects.filter(assigned_to=request.user)
    
    context = {
        'tasks': tasks,
        'user': request.user,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check permissions
    if request.user.role == 'USER' and task.assigned_to != request.user:
        raise PermissionDenied("You do not have permission to view this task")
    
    if request.user.role == 'ADMIN' and task.assigned_to.admin != request.user:
        raise PermissionDenied("You do not have permission to view this task")
    
    context = {
        'task': task,
        'user': request.user,
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def user_list(request):
    if not request.user.is_superadmin:
        raise PermissionDenied("Only SuperAdmin can access this page")
    
    users = User.objects.all()
    context = {
        'users': users,
        'user': request.user,
    }
    return render(request, 'tasks/user_list.html', context)

@login_required
def admin_list(request):
    if not request.user.is_superadmin:
        raise PermissionDenied("Only SuperAdmin can access this page")
    
    admins = User.objects.filter(role__in=['ADMIN', 'SUPERADMIN'])
    context = {
        'admins': admins,
        'user': request.user,
    }
    return render(request, 'tasks/panel_list.html', context)