from django.contrib import admin
from tasktracker.models import ProjectModel,TaskModel
# Register your models here.
admin.site.register(ProjectModel)
admin.site.register(TaskModel)
