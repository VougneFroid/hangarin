"""
URL configuration for hangarinsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todohan.views import HomePageView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView
from todohan.views import NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView, SubTaskListView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView, PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from todohan import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('pwa.urls')),
    path("accounts/", include("allauth.urls")), # allauth routes
    path('', views.HomePageView.as_view(), name='home'),
    path('task_list', TaskListView.as_view(), name='task-list'),
    path('task_list/add', TaskCreateView.as_view(), name='task-add'),
    path('task_list/<pk>',TaskUpdateView.as_view(), name='task-update'),
    path('task_list/<pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/add/', NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/edit/', SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),
    path('priorities/', views.PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', views.PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/edit/', views.PriorityUpdateView.as_view(), name='priority-edit'),
    path('priorities/<int:pk>/delete/', views.PriorityDeleteView.as_view(), name='priority-delete'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]
