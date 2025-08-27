from django.contrib import admin

# Register your models here.
from .models import Priority, Category, Task, Note, SubTask

admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Note)
admin.site.register(SubTask)
