from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeSerializer, EmployeeRegistrationSerializer, EmployeeLoginSerializer


class EmployeeRegistrationView(APIView):

    def post(self, request):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(APIView):

    def post(self, request):
        serializer = EmployeeLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Logged in Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(data={"message": "Logout successfully"}, status=status.HTTP_200_OK)


class EmployeeListView(ListAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
