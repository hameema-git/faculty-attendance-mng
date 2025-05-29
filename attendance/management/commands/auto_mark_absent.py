# attendance/management/commands/auto_mark_absent.py

# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from attendance.models import Attendance, CustomUser

# class Command(BaseCommand):
#     help = 'Automatically mark absent for faculty who did not record attendance today'

#     def handle(self, *args, **kwargs):
#         today = timezone.now().date()
#         faculty_users = CustomUser.objects.filter(is_faculty=True)
#         count = 0

#         for faculty in faculty_users:
#             if not Attendance.objects.filter(faculty=faculty, date=today).exists():
#                 Attendance.objects.create(
#                     faculty=faculty,
#                     date=today,
#                     status='A',  # Absent
#                     approved=True,  # Or False if you want admin approval
#                     hours_worked=0
#                 )
#                 count += 1

#         self.stdout.write(self.style.SUCCESS(f"Marked {count} faculty as Absent for {today}"))

# attendance/management/commands/auto_mark_absent.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Attendance, CustomUser

class Command(BaseCommand):
    help = 'Automatically mark absent for faculty who did not record attendance today'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        faculty_users = CustomUser.objects.filter(is_faculty=True)
        count = 0

        for faculty in faculty_users:
            if not Attendance.objects.filter(faculty=faculty, date=today).exists():
                Attendance.objects.create(
                    faculty=faculty,
                    date=today,
                    status='A',  # Absent
                    approved=True,
                    hours_worked=0
                )
                count += 1

        # Commented out to avoid cron-job.org output overflow
        # self.stdout.write(self.style.SUCCESS(f"Marked {count} faculty as Absent for {today}"))

