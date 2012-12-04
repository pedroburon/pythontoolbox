from django.contrib import admin

from .models import Project, Category, Group


class CategoryInline(admin.TabularInline):
    model = Category


class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = [CategoryInline]


admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Group, GroupAdmin)
