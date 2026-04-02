from django.contrib import admin
from .models import Doctor, Department, Appointment, ContactMessage, UserProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'department', 'experience', 'rating', 'available')
    list_filter = ('available', 'department')
    search_fields = ('name', 'specialization')
    list_editable = ('available',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('status',)
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

# Register your models here.
