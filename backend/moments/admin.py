from django.contrib import admin
from .models import Moment

@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):  # <--- 注意这里改成了 admin.ModelAdmin
    list_display = ('id', 'author', 'type', 'created_at')
    list_filter = ('type', 'created_at')