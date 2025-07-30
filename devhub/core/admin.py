from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PythonUser

@admin.register(PythonUser)
class PythonUserAdmin(UserAdmin):
    model = PythonUser

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'location',
                'company_name',
                'occupation',
                'about_me',
                'followers',
                'profile_pic',
                'projects_descriptions',
                'custom_message',
                'hired_users',
                'can_add_projects',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'location',
                'company_name',
                'occupation',
                'about_me',
                'followers',
                'profile_pic',
                'projects_descriptions',
                'custom_message',
                'hired_users',
                'can_add_projects',
            ),
        }),
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'location',
        'company_name',
        'occupation',
        'can_add_projects',
        'is_staff',
    )
    search_fields = ('username', 'email', 'company_name', 'occupation')
    list_filter = ('can_add_projects', 'is_staff', 'is_active')
