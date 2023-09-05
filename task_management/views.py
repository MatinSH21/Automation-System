from rest_framework.views import APIView, Response, Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(author=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        not_allowed_fields = ['id', 'author', 'created_date', 'updated_date']
        fields_list = []

        # Check if the request contains some unchangeable fields
        for field in request.data:
            if field in not_allowed_fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {"detail": f"Field '{fields_list[0]}' value cannot be set by manually."}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {"detail": f"{fields_list} values cannot be set by manually."}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskCreateSerializer(data=request.data)

        # Check if request contains fields that are not included in Task model
        for field in request.data:
            if field not in serializer.fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {"detail": f"Task model doesn't have '{fields_list[0]}' field"}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {"detail": f"Task model doesn't have {fields_list} fields"}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        if task.author != request.user:
            return Response({"detail": "You don't have permission to view this task"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        task = self.get_object(pk)
        if task.author != request.user:
            return Response({"detail": "You don't have permission to update this task"},
                            status=status.HTTP_403_FORBIDDEN)

        not_allowed_fields = ['id', 'author', 'created_date', 'updated_date']
        fields_list = []

        # Check if the request contains some unchangeable fields
        for field in request.data:
            if field in not_allowed_fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {"detail": f"Field '{fields_list[0]}' cannot be updated."}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {"detail": f"{fields_list} fields cannot be updated."}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(instance=task, data=request.data, partial=True)

        # Check if request contains fields that are not included in Task model
        for field in request.data:
            if field not in serializer.fields:
                fields_list.append(field)
        if len(fields_list) == 1:
            data = {"detail": f"Task model doesn't have '{fields_list[0]}' field"}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif fields_list:
            data = {"detail": f"Task model doesn't have {fields_list} fields"}
            fields_list.clear()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task.author != request.user:
            return Response({"detail": "You don't have permission to delete this task"},
                            status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response({"detail": "Task got deleted"}, status=status.HTTP_204_NO_CONTENT)
