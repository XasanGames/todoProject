from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, task_list, add_task
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from .views import RegisterView, LoginView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('', task_list, name='task-list'),  # Главная страница с задачами
    path('add/', add_task, name='add-task'),  # Страница для добавления задачи
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('login/', LoginView.as_view(), name='login'),  # HTML-страница входа
]



