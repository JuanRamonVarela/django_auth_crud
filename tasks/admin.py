from django.contrib import admin
from .models import tasks
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields=("created", "id")
admin.site.register(tasks, TaskAdmin)