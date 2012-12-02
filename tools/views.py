from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Group, Project, Category


class GroupListView(ListView):
    model = Group


class CategoryListView(ListView):
    model = Category


class ProjectListView(ListView):
    model = Project

    def dispatch(self, request, letter):
        self.first_letter = letter
        return super(ProjectListView, self).dispatch(request=request)

    def get_context_data(self, object_list):
        context = super(ProjectListView, self).get_context_data(object_list=object_list)
        context.update({'first_letter': self.first_letter})
        return context

    def get_queryset(self):
        queryset = super(ProjectListView, self).get_queryset()
        return queryset.filter(name__startswith=self.first_letter)


class ProjectListByCategoryView(ListView):
    model = Project
    template_name = 'tools/project_list_by_category.html'

    def dispatch(self, request, category):
        self.category = get_object_or_404(Category, slug=category)
        return super(ProjectListByCategoryView, self).dispatch(request=request)

    def get_context_data(self, object_list):
        context = super(ProjectListByCategoryView, self).get_context_data(object_list=object_list)
        context.update({'category': self.category})
        return context

    def get_queryset(self):
        queryset = super(ProjectListByCategoryView, self).get_queryset()
        return queryset.filter(category=self.category)
