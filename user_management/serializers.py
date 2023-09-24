from rest_framework import serializers
from .models import Employee, Profile


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        employee = Employee(**validated_data)
        employee.set_password(password)
        employee.save()
        return employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'username', 'date_created', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileWithRoleSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    role = serializers.StringRelatedField(source='employee.role')

    def to_representation(self, instance):
        profile_data = ProfileSerializer(instance.profile).data
        return {'profile': profile_data, 'role': instance.role}
