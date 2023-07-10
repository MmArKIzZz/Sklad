from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import OrderOut


class OrderOutAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='View All Orders').exists():
            return qs  # Показывать все запросы для суперпользователей и администраторов группы "View All Orders"
        elif request.user.groups.filter(name='work').exists():
            return qs  # Показывать все запросы для пользователей из группы "work"
        return qs.filter(user=request.user)  # Показывать только запросы текущего пользователя

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            if not request.user.is_superuser and not request.user.groups.filter(name='View All Orders').exists():
                kwargs["queryset"] = User.objects.filter(pk=request.user.pk)  # Ограничить выбор пользователей только текущим пользователем
            else:
                kwargs["queryset"] = User.objects.all()  # Разрешить выбор всех пользователей для суперпользователя и пользователей из группы "View All Orders"
        elif db_field.name == "worker" and request.user.groups.filter(name='work').exists():
            kwargs["queryset"] = User.objects.filter(groups__name='work')  # Ограничить выбор пользователей только из группы "work"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.groups.filter(name='work').exists():
            readonly_fields = [field.name for field in self.model._meta.fields if field.name not in ['worker', 'status']]
        return readonly_fields

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.groups.filter(name='work').exists():
            fields = ['worker', 'status']
        return fields

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='work').exists():
            obj.worker = request.user  # Устанавливаем поле "worker" только на текущего пользователя из группы "work"
        super().save_model(request, obj, form, change)


admin.site.register(OrderOut, OrderOutAdmin)

