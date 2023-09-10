from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import Employee, Profile, Role, Permission


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):

    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email']
    list_display = ['username', 'email', 'is_active', 'is_staff']
    ordering = ['date_created']
    inlines = [ProfileInline]
    actions = ['activation_action']

    fieldsets = [
        (None, {'fields': ('username', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'role')})
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')})
    ]

    def activation_action(self, request, queryset):
        queryset.update(is_active=True)
    activation_action.short_description = "Active selected employees"


admin.site.unregister(Group)
admin.site.register(Role)
admin.site.register(Permission)
