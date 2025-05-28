
# Create your models here.
# attendance/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_faculty = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # optional, just for clarity

    def __str__(self):
        return self.username
    
class FacultyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    joining_date = models.DateField()
    department = models.CharField(max_length=100)
    personal_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


# from django.utils import timezone

# class Attendance(models.Model):
#     STATUS_CHOICES = [
#         ('P', 'Present'),
#         ('A', 'Absent'),
#         ('L', 'Leave'),
#         ('OA', 'Optional Absent'),  # Set by admin
#     ]

#     faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     date = models.DateField(default=timezone.now)
#     status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='A')
#     approved = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('faculty', 'date')  # only one record per day per faculty

#     def __str__(self):
#         return f"{self.faculty.username} - {self.date} - {self.status}"

from django.db import models
from django.utils import timezone
from django.conf import settings

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
        ('OA', 'Optional Absent'),  # Set by admin
    ]

    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='A')
    approved = models.BooleanField(default=False)

    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # e.g., 4.5 hours
    message = models.TextField(blank=True, null=True)  # Optional message from faculty

    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)
    # updated_at = models.DateTimeField(auto_now=True,default=timezone.now)

    class Meta:
        unique_together = ('faculty', 'date')

    def __str__(self):
        return f"{self.faculty.username} - {self.date} - {self.status} - {self.hours_worked} hrs"


