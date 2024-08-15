from django.urls import path
from .views import TodoListView, TodoDetailView, TodoCreateView, TodoUpdateView, TodoCompleteView, TodoDeleteView
from django.contrib.auth import views as auth_views
from .views import todo_list, todo_complete, todo_delete

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


# API 문서화 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Todo API",
        default_version='v1',
        description="API documentation for Todo App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API 관련 URL 패턴
    path('api/todos/', TodoListView.as_view(), name='todo-list'),
    path('api/todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('api/todos/create/', TodoCreateView.as_view(), name='todo-create'),
    path('api/todos/<int:pk>/update/', TodoUpdateView.as_view(), name='todo-update'),
    path('api/todos/<int:pk>/complete/', TodoCompleteView.as_view(), name='todo-complete'),
    path('api/todos/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo-delete'),

    # 인증 관련 URL 패턴
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 웹 페이지 관련 URL 패턴
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', todo_list, name='todo-list'),
    path('complete/<int:pk>/', todo_complete, name='todo-complete'),
    path('delete/<int:pk>/', todo_delete, name='todo-delete'),
]
