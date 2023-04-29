from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.models import User
from todo.models import Todo
from todo.serializers import TodoSerializer, TodoCreateSerializer

class TodoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TodoShowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            todo = Todo.objects.filter(user_id=user_id)
            serializer = TodoSerializer(todo, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class TodoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, article_id):
        user = get_object_or_404(User, id=user_id)
        todo = Todo.objects.get(id=todo_id)
        if request.user == user:
            serializer = TodoCreateSerializer(todo, data=request.data)
            if serializer.is_valid():
                if request.data.get("is_completed") == True:
                    serializer.save(completed_at=timezone.now())
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)    

    def delete(self, request, todo_id, user_id):
        user = get_object_or_404(User, id=user_id)
        todo = Todo.objects.get(id=todo_id)
        if request.user == user:
            todo.delete()
            return Response("삭제 했습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

