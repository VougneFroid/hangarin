from django.shortcuts import render
from django.views.generic.list import ListView
from todohan.models import Priority, Task, Note, SubTask, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from todohan.forms import TaskForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "recent_tasks"
    paginate_by = 5
    ordering = ['-created_at']

    def get_queryset(self):
        # Show only the most recent tasks
        return Task.objects.order_by('-created_at')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # General Stats
        context["total_tasks"] = Task.objects.count()
        context["completed_tasks"] = Task.objects.filter(status="Completed").count()
        context["pending_tasks"] = Task.objects.exclude(status="Completed").count()
        context["total_notes"] = Note.objects.count()
        context["total_subtasks"] = SubTask.objects.count()
        context["total_priorities"] = Priority.objects.count()
        context["total_categories"] = Category.objects.count()

        # Top 3 Priorities (by task count)
        context["top_priorities"] = (
            Priority.objects.annotate(task_count=models.Count("task"))
            .order_by("-task_count")[:3]
        )

        # Top 3 Categories (by task count)
        context["top_categories"] = (
            Category.objects.annotate(task_count=models.Count("task"))
            .order_by("-task_count")[:3]
        )

        return context

    
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'deadline')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        # Validate sort_by to prevent errors
        allowed_sort_fields = [
            'deadline', 'title', 'status', 'category__name', 'priority__name'
        ]
        if sort_by not in allowed_sort_fields:
            sort_by = 'deadline'
        return qs.order_by(sort_by, 'status')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'created_at')

        if query:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query)
            )

        allowed_sort_fields = [
            'created_at', 'updated_at', 'content', 'task__title'
        ]
        if sort_by not in allowed_sort_fields:
            sort_by = 'created_at'

        return qs.order_by(sort_by)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")
    

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "note_del.html"
    success_url = reverse_lazy("note-list")

class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = "subtask_list.html"
    context_object_name = "subtasks"
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'created_at')

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(parent_task__title__icontains=query)
            )

        allowed_sort_fields = [
            'created_at', 'updated_at', 'title', 'status', 'parent_task__title'
        ]
        if sort_by not in allowed_sort_fields:
            sort_by = 'created_at'

        return qs.order_by(sort_by, 'status')

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = "subtask_del.html"
    success_url = reverse_lazy("subtask-list")

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'name')

        if query:
            qs = qs.filter(Q(name__icontains=query))

        allowed_sort_fields = ['name', 'created_at', 'updated_at']
        if sort_by not in allowed_sort_fields:
            sort_by = 'name'

        return qs.order_by(sort_by)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category_del.html"
    success_url = reverse_lazy("category-list")

class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = "priority_list.html"
    context_object_name = "priorities"
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'name')

        if query:
            qs = qs.filter(Q(name__icontains=query))

        allowed_sort_fields = ['name', 'created_at', 'updated_at']
        if sort_by not in allowed_sort_fields:
            sort_by = 'name'

        return qs.order_by(sort_by)


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    fields = ['name']
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    fields = ['name']
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = "priority_del.html"
    success_url = reverse_lazy("priority-list")
