from django.shortcuts import render
from django.views.generic.list import ListView
from todohan.models import Priority, Task, Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from todohan.forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'home'
    template_name = 'home.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_task"] = Task.objects.count()

        current_year = timezone.now().year
        context["task_added_this_year"] = Task.objects.filter(created_at__year=current_year).count()

        context["total_notes"] = Note.objects.count()

        context["total_priorities"] = Priority.objects.count()

        return context

    
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5

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


