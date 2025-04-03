from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from .models import Task
from django.utils import timezone
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.contrib.auth.models import User

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

def task_list(request):
    tasks = Task.objects.all()  # Получаем все задачи
    return render(request, 'index.html', {'tasks': tasks})

from django.shortcuts import render, redirect
from .forms import TaskForm  # Импортируем форму для добавления задачи

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  # Получаем данные из формы
        if form.is_valid():
            form.save()  # Сохраняем задачу в базе данных
            return redirect('task-list')  # Перенаправляем на страницу списка задач
    else:
        form = TaskForm()  # Пустая форма для добавления новой задачи

    return render(request, 'add_task.html', {'form': form})

# Сериализатор для регистрации пользователей
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

# API-вью для регистрации
class RegisterView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'register.html', {'csrf_token': csrf_token})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return data

class LoginView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'login.html', {'csrf_token': csrf_token})
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    