from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    EmployeeRegistrationSerializer,
    EmployeeSerializer,
    ProfileSerializer,
    ProfileWithRoleSerializer
)
from .models import Employee
from .permissions import IsManager, IsAdmin


class EmployeeRegistrationAPIView(APIView):
    permission_classes = [IsManager | IsAdmin]

    def post(self, request):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role == "manager":
                if serializer.validated_data['role'] != 'employee':
                    data = {"detail": "Manager can only assign employee role."}
                    return Response(data, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(TokenObtainPairView):
    pass


class EmployeeListAPIView(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get(self, request):
        if request.user.role == "manager":
            employees = Employee.objects.filter(role='employee')
        elif request.user.role == "admin":
            employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = ProfileWithRoleSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get_employee(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        user = request.user
        employee = self.get_employee(pk)
        if user.role == "manager" and employee.role != "employee":
            data = {"detail": "You don't have permission to access this profile"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        profile = employee.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        employee = self.get_employee(pk)
        user = request.user
        if user.role == "manager" and employee.role != "employee":
            data = {"detail": "You don't have permission to access this profile"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        if user.role == "admin" and employee.role == "admin":
            data = {"detail": "You don't have permission to access this profile"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        profile = employee.profile

        not_allowed_fields = ['id', 'employee', 'date_updated']
        fields_list = []

        # Check if request contains value for fields that are not changeable
        for field in request.data:
            if field in not_allowed_fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {'detail': f"Field '{fields_list[0]}' value cannot change"}
            fields_list.clear()
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {'detail': f"{fields_list} values cannot change"}
            fields_list.clear()
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        # Check if request contains fields that are not included in Profile model
        for field in request.data:
            if field not in serializer.fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {'detail': f"Profile model doesn't have '{fields_list[0]}' field"}
            fields_list.clear()
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {'detail': f"Profile model doesn't have {fields_list} fields"}
            fields_list.clear()
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
