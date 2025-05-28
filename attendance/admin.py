from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FacultyProfile, Attendance

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_faculty', 'is_admin']
    list_filter = ['is_faculty', 'is_admin']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_faculty', 'is_admin')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Faculty Profile
@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    # list_display = ['user', 'department', 'joining_date']
    # list_display = ['user','First Name','Last Name', 'department', 'joining_date', 'personal_phone', 'guardian_phone']
    list_display = ['get_username', 'get_full_name', 'department', 'joining_date', 'personal_phone', 'guardian_phone']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

# Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'date', 'status', 'approved']
    list_filter = ['date', 'status', 'approved']
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(approved=True)
    approve_selected.short_description = "Approve selected attendances"
