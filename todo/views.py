from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class TodoListPagination(PageNumberPagination):
    page_size = 10  # 한 페이지에 보여줄 Todo 항목 수

class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoListPagination  # 페이징 설정
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    ordering_fields = ['created_at', 'title']  # 정렬할 수 있는 필드 설정
    filterset_fields = ['is_completed']
    search_fields = ['title']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoDetailView(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'

class TodoCreateView(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'

class TodoCompleteView(APIView):
    def post(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            todo.is_completed = True
            todo.save()
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TodoDeleteView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    lookup_field = 'pk'

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Todo

@login_required
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(user=request.user, title=title)  # Todo 생성 시 사용자 연결
        return redirect('todo-list')

    todos = Todo.objects.filter(user=request.user)  # 로그인된 사용자에 따른 필터링
    return render(request, 'todo_list.html', {'todos': todos})

@login_required
def todo_complete(request, pk):
    todo = Todo.objects.get(pk=pk, user=request.user)  # 사용자와 연결된 Todo만 조회
    todo.is_completed = True
    todo.save()
    return redirect('todo-list')

@login_required
def todo_delete(request, pk):
    todo = Todo.objects.get(pk=pk, user=request.user)  # 사용자와 연결된 Todo만 삭제
    todo.delete()
    return redirect('todo-list')
