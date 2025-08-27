from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from todohan.models import Category, Priority, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_tasks(10)
        self.create_notes(10)
        self.create_subtasks(10)

    def create_tasks(self, count):
        fake = Faker()
        
        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            task_name = ' '.join(words)
            Task.objects.create(
                title=task_name.title(),
                description=fake.sentence(nb_words=5),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                category=Category.objects.order_by('?').first(),
                priority=Priority.objects.order_by('?').first()
            )
        self.stdout.write(self.style.SUCCESS(f'Initial data for tasks created successfully.'))

    
    def create_notes(self, count):
        fake = Faker()

        for _ in range(count):
            Note.objects.create(
                task=Task.objects.order_by('?').first(),
                content=fake.paragraph(nb_sentences=3)
            )
        self.stdout.write(self.style.SUCCESS(f'Initial data for notes created successfully.'))

    def create_subtasks(self, count):
        fake=Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            subtask_name = ' '.join(words)
            SubTask.objects.create(
                parent_task=Task.objects.order_by('?').first(),
                title=subtask_name.title(),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )
        self.stdout.write(self.style.SUCCESS(f'Initial data for subtasks created successfully.'))



