from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmployeeRegistrationSerializer, EmployeeSerializer, ProfileSerializer


class EmployeeRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(TokenObtainPairView):
    pass


class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = request.user
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profile

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
