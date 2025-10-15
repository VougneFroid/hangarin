from django import forms
from django.forms import ModelForm
from .models import Task, Note, SubTask


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = '__all__'

class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = '__all__'
