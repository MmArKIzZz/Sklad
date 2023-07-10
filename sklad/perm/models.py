from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # для суперпользователя отображаются все записи

        # Для обычных пользователей отображаются только их собственные записи
        return qs.filter(user=request.user)