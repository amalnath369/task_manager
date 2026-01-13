from rest_framework import serializers
from .models import Task
from users.models import User


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'assigned_by', 'assigned_by_username', 'due_date', 'status',
            'completion_report', 'worked_hours', 'completed_at',
            'created_at', 'updated_at', 'created_by', 'created_by_username',
            'updated_by', 'updated_by_username'
        ]
        read_only_fields = [
            'completed_at', 'created_at', 'updated_at', 
            'created_by', 'updated_by', 'assigned_by'
        ]
    
    def validate(self, data):
        if self.instance and self.instance.status == 'COMPLETED':
            # Prevent modifying completed tasks
            if any(field in data for field in ['title', 'description', 'assigned_to', 'due_date']):
                raise serializers.ValidationError("Cannot modify completed tasks")
        
        # Check if status is being changed to COMPLETED
        if 'status' in data and data['status'] == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when marking task as completed'
                })
            if not data.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours are required when marking task as completed'
                })
        
        return data
    
    def create(self, validated_data):
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required'
                })
            if not data.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours are required'
                })
        return data


class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username')
    assigned_to_email = serializers.CharField(source='assigned_to.email')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to_username', 
            'assigned_to_email', 'due_date', 'completion_report', 
            'worked_hours', 'completed_at', 'created_at'
        ]