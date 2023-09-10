from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.utils import OperationalError

from user_management.models import Role, Permission


class Command(BaseCommand):
    help = "Create custom permissions for roles"

    def handle(self, *args, **options):

        # All custom permissions
        custom_permissions = [
            {
                'name': 'Can create task',
                'codename': 'can_create_task'
            },
            {
                'name': 'Can view task',
                'codename': 'can_view_task'
            },            {
                'name': 'Can update task',
                'codename': 'can_update_task'
            },            {
                'name': 'Can delete task',
                'codename': 'can_delete_task'
            },
            {
                'name': 'Can create employee',
                'codename': 'can_create_employee'
            },
            {
                'name': 'Can view employee',
                'codename': 'can_view_employee'
            },
            {
                'name': 'Can update employee',
                'codename': 'can_update_employee'
            },
            {
                'name': 'Can delete employee',
                'codename': 'can_delete_employee'
            },
        ]

        try:
            # Check if user_management app is installed
            if not apps.is_installed('user_management'):
                self.stdout.write(self.style.ERROR(
                    "The 'user_management' app is not installed in Django. "
                    "Make sure it's included in your project's settings."
                ))
                return

            # Check if Permission and Role model exist
            if not apps.get_model('user_management', 'Permission') or not apps.get_model("user_management", "Role"):
                self.stdout.write(self.style.ERROR(
                    "The 'Permission' and 'Role' models do not exist in the 'user_management' app."
                    " Make sure the models are defined and migrated."))
                return

            # Create Administrator role
            role, created = Role.objects.get_or_create(name='Administrator')
            if created:
                self.stdout.write(self.style.SUCCESS('Created role: Administrator'))

            # Create those Permissions and assign them to Administrator
            for permission_data in custom_permissions:
                permission, created = Permission.objects.get_or_create(
                    name=permission_data['name'],
                    codename=permission_data['codename']
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created permission: {permission_data['name']}"))
                role.permissions.add(permission)

            self.stdout.write(self.style.SUCCESS('Assigned permissions to role: Administrator'))

        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Database connection error: {e}"))
