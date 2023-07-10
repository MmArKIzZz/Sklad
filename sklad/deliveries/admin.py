from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Delivers


class DeliversAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='View All Orders').exists():
            return qs  # Показывать все запросы для суперпользователей и администраторов группы "View All Orders"
        return qs.filter(user=request.user)  # Показывать только запросы текущего пользователя

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            if request.user.is_superuser or request.user.groups.filter(name='View All Orders').exists():
                kwargs["queryset"] = User.objects.filter(groups__name='seller')  # Ограничить выбор пользователей только из группы "seller"
            elif not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(pk=request.user.pk)  # Ограничить выбор пользователей только текущим пользователем
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Delivers, DeliversAdmin)



