from rest_framework import serializers
from .models import Task
from user_management.models import Employee


class EmployeeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            return Employee.objects.get(username=data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee with this username does not exist.")


class TaskSerializer(serializers.ModelSerializer):
    author = EmployeeField(queryset=Employee.objects.all())
    assigned_to = EmployeeField(queryset=Employee.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    assigned_to = EmployeeField(queryset=Employee.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'
