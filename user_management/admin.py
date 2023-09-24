from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import Employee, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):

    list_filter = ['is_staff', 'is_active', 'is_superuser', 'role']
    search_fields = ['username']
    list_display = ['username', 'role', 'is_active', 'id']
    ordering = ['date_created']
    inlines = [ProfileInline]
    actions = ['activation_action']

    fieldsets = [
        (None, {'fields': ('username', )}),
        ('Permissions', {'fields': ('is_active', 'role')})
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active',)})
    ]

    def activation_action(self, request, queryset):
        queryset.update(is_active=True)
    activation_action.short_description = "Active selected employees"


admin.site.unregister(Group)
