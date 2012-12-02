from django.contrib import admin

from .models import Project, Category, Group


admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Group)
