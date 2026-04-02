from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='🏥')

    def _str_(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    bio = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Dr. {self.name} ({self.specialization})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.department} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Message from {self.name} – {self.created_at.strftime('%d %b %Y')}"

    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    def _str_(self):
        return f"Profile: {self.user.username}"
# Create your models here.
