from django.contrib.auth.models import User  # User 모델 추가
from django.db import models

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Todo 항목을 사용자와 연결
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
