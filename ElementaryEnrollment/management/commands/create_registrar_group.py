# filepath: /d:/Projects/EnrollmentSystem/ElementaryEnrollment/management/commands/create_registrar_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ElementaryEnrollment.models import Student, Enrollment

class Command(BaseCommand):
    help = 'Create Registrar group and assign permissions'

    def handle(self, *args, **kwargs):
        # Create the Registrar group
        registrar_group, created = Group.objects.get_or_create(name='Registrar')

        # Assign permissions to the Registrar group
        models = [Student, Enrollment]  # Add other models as needed
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            registrar_group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created Registrar group and assigned permissions'))