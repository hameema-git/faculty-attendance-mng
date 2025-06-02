from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Attendance
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed



# def faculty_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user and user.is_faculty:
#             login(request, user)
#             return redirect('faculty_dashboard')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials or not faculty'})
#     # return render(request, 'login.html')
#     return render(request, "attendance/login.html", {"form": form})

def faculty_login(request):
    if request.method == "POST":
        # username = request.POST['username']
        # password = request.POST['password']
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'is_faculty') and user.is_faculty:
            login(request, user)
            return redirect('faculty_dashboard')
        else:
            return render(request, 'attendance/login.html', {'error': 'Invalid credentials or not faculty'})
    
    return render(request, "attendance/login.html")

# @login_required
# def faculty_dashboard(request):
#     today = date.today()
#     attendance_exists = Attendance.objects.filter(faculty=request.user, date=today).exists()
#     return render(request, "attendance/dashboard.html", {
#         'attendance_exists': attendance_exists
#     })

# @login_required
# def faculty_dashboard(request):
#     today = date.today()
#     attendance_exists = Attendance.objects.filter(faculty=request.user, date=today).exists()
#     return render(request, "attendance/dashboard.html", {
#         'attendance_exists': attendance_exists,
#         'today': today  # Pass current date to template
#     })
# @login_required
# def mark_attendance(request):
#     today = date.today()
#     already_marked = Attendance.objects.filter(faculty=request.user, date=today).exists()
#     if not already_marked:
#         Attendance.objects.create(faculty=request.user, date=today, status='P')
#     return redirect('faculty_dashboard')


from django.contrib.admin.views.decorators import staff_member_required

# @staff_member_required
# def admin_dashboard(request):
#     return render(request, "attendance/admin_dashboard.html")


# def admin_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user and user.is_admin:
#             login(request, user)
#             return redirect('admin_dashboard')
#         else:
#             return render(request, 'admin/login.html', {'error': 'Invalid admin credentials'})
#     return render(request, 'admin/login.html')


def admin_login(request):
    if request.method == "POST":
        # username = request.POST["username"]
        # password = request.POST["password"]
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'is_admin') and user.is_admin:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "attendance/admin_login.html", {"error": "Invalid credentials or not an admin"})

    return render(request, "attendance/admin_login.html")

# @login_required(login_url='/admin/login/')
# def admin_dashboard(request):
#     if not request.user.is_admin:
#         return redirect('faculty_dashboard')  # or raise 403
#     return render(request, 'admin/dashboard.html')

def home(request):
    return render(request, 'attendance/home.html')


from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('home')  # or show access denied
    return render(request, 'attendance/admin_dashboard.html')

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .models import CustomUser, Attendance
from attendance.forms import FacultyForm  # You need to define this form
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('home')  # Or 'faculty_login' or 'admin_login' if you prefer


def admin_view_faculty(request):
    faculty_list = CustomUser.objects.filter(is_faculty=True)
    return render(request, 'attendance/admin_view_faculty.html', {'faculty_list': faculty_list})

# def admin_view_attendance(request):
#     attendance_list = Attendance.objects.all().order_by('-date')
#     return render(request, 'attendance/admin_view_attendance.html', {'attendance_list': attendance_list})

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def admin_view_attendance(request):
    # search_name = request.GET.get('name', '').strip()
    search_date = request.GET.get('date', '').strip()
    month_year = request.GET.get('month_year')
    selected_month = selected_year = None

    # Academic year: May 2025 to March 2026
    academic_start = date(2025, 5, 1)
    academic_end = date(2026, 3, 31)

    attendance_list = Attendance.objects.filter(date__range=(academic_start, academic_end))

    # if search_name:
    #     attendance_list = attendance_list.filter(faculty__username__icontains=search_name)
    search_name = request.GET.get('name', '').strip()
    if search_name:
        attendance_list = attendance_list.filter(
            Q(faculty__first_name__icontains=search_name) |
            Q(faculty__last_name__icontains=search_name) |
            Q(faculty__username__icontains=search_name)
        )

    if search_date:
        attendance_list = attendance_list.filter(date=search_date)
    elif month_year:
        try:
            selected_month, selected_year = map(int, month_year.split('-'))
            attendance_list = attendance_list.filter(
                date__month=selected_month,
                date__year=selected_year
            )
        except ValueError:
            pass
    else:
        # Default to current month if within academic year
        today = date.today()
        if academic_start <= today <= academic_end:
            selected_month = today.month
            selected_year = today.year
            attendance_list = attendance_list.filter(
                date__month=selected_month,
                date__year=selected_year
            )

    attendance_list = attendance_list.order_by('-date')

    # Generate academic year months: May 2025 to March 2026
    months = []
    current = academic_start
    while current <= academic_end:
        months.append({
            'month': current.month,
            'year': current.year,
            'label': current.strftime("%B %Y"),
            'value': f"{current.month}-{current.year}"
        })
        current += relativedelta(months=1)

    return render(request, 'attendance/admin_view_attendance.html', {
        'attendance_list': attendance_list,
        'search_name': search_name,
        'search_date': search_date,
        'months': months,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })


def admin_add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view_faculty')
    else:
        form = FacultyForm()
    return render(request, 'attendance/admin_add_faculty.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Attendance,FacultyProfile

# def admin_approve_attendance(request):
#     pending_attendance = Attendance.objects.filter(approved=False)
#     if request.method == 'POST':
#         ids = request.POST.getlist('attendance_ids')
#         Attendance.objects.filter(id__in=ids).update(approved=True)
#         return redirect('admin_approve_attendance')
#     return render(request, 'attendance/admin_approve_attendance.html', {'attendances': pending_attendance})

from django.db.models import Q

def admin_approve_attendance(request):
    # search_name = request.GET.get('name', '').strip()
    search_date = request.GET.get('date', '').strip()
    month_year = request.GET.get('month_year')
    selected_month = selected_year = None

    # Academic Year Range: May 2025 – March 2026
    academic_start = date(2025, 5, 1)
    academic_end = date(2026, 3, 31)

    pending_attendance = Attendance.objects.filter(approved=False, date__range=(academic_start, academic_end))

    # if search_name:
    #     pending_attendance = pending_attendance.filter(faculty__username__icontains=search_name)
    search_name = request.GET.get('name', '').strip()
    if search_name:
        pending_attendance = pending_attendance.filter(
            Q(faculty__first_name__icontains=search_name) |
            Q(faculty__last_name__icontains=search_name) |
            Q(faculty__username__icontains=search_name)
        )

    if search_date:
        pending_attendance = pending_attendance.filter(date=search_date)
    elif month_year:
        try:
            selected_month, selected_year = map(int, month_year.split('-'))
            pending_attendance = pending_attendance.filter(
                date__month=selected_month,
                date__year=selected_year
            )
        except ValueError:
            pass
    else:
        # Default to current month if within academic year
        today = date.today()
        if academic_start <= today <= academic_end:
            selected_month = today.month
            selected_year = today.year
            pending_attendance = pending_attendance.filter(
                date__month=selected_month,
                date__year=selected_year
            )

    if request.method == 'POST':
        ids = request.POST.getlist('attendance_ids')
        Attendance.objects.filter(id__in=ids).update(approved=True)
        return redirect('admin_approve_attendance')

    # Generate academic months (May 2025 – March 2026)
    months = []
    current = academic_start
    while current <= academic_end:
        months.append({
            'month': current.month,
            'year': current.year,
            'label': current.strftime("%B %Y"),
            'value': f"{current.month}-{current.year}"
        })
        current += relativedelta(months=1)

    return render(request, 'attendance/admin_approve_attendance.html', {
        'attendances': pending_attendance,
        'search_name': search_name,
        'search_date': search_date,
        'months': months,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })

@login_required
def faculty_dashboard(request):
    today = date.today()
    attendance_exists = Attendance.objects.filter(faculty=request.user, date=today).exists()
    return render(request, "attendance/faculty_dashboard.html", {
        'attendance_exists': attendance_exists,
        'today': today
    })

# @login_required
# def faculty_attendance_history(request):
#     records = Attendance.objects.filter(faculty=request.user).order_by('-date')
#     return render(request, "attendance/faculty_history.html", {'records': records})
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

@login_required
def faculty_attendance_history(request):
    month_year = request.GET.get('month_year')
    search_date = request.GET.get('date', '').strip()

    # Academic year range
    academic_start = date(2025, 5, 1)
    academic_end = date(2026, 5, 31)

    records = Attendance.objects.filter(
        faculty=request.user,
        date__range=(academic_start, academic_end)
    )

    selected_month = selected_year = None

    if search_date:
        try:
            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            records = records.filter(date=search_date_obj)
        except ValueError:
            pass

    elif month_year:
        try:
            selected_month, selected_year = map(int, month_year.split('-'))
            records = records.filter(date__month=selected_month, date__year=selected_year)
        except ValueError:
            pass

    else:
        # Default to current month if no filters applied
        today = date.today()
        if academic_start <= today <= academic_end:
            selected_month = today.month
            selected_year = today.year
            records = records.filter(date__month=selected_month, date__year=selected_year)

    records = records.order_by('-date')

    # Generate academic year month list (June 2025 to May 2026)
    months = []
    current = academic_start
    while current <= academic_end:
        months.append({
            'month': current.month,
            'year': current.year,
            'label': current.strftime("%B %Y"),
            'value': f"{current.month}-{current.year}"
        })
        current += relativedelta(months=1)

    return render(request, "attendance/faculty_history.html", {
        'records': records,
        'months': months,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'search_date': search_date,
    })


# def admin_delete_faculty(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     user.delete()
#     return redirect('admin_view_faculty')

@login_required
def admin_delete_faculty(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('admin_view_faculty')  # or use messages for confirmation

    return render(request, 'attendance/confirm_delete_faculty.html', {'user': user})

# def admin_edit_faculty(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     faculty_profile = get_object_or_404(FacultyProfile, user=user)

#     class EditFacultyForm(UserCreationForm):
#         first_name = forms.CharField(initial=user.first_name)
#         last_name = forms.CharField(initial=user.last_name)
#         email = forms.EmailField(initial=user.email)
#         department = forms.CharField(initial=faculty_profile.department)
#         joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=faculty_profile.joining_date)
#         personal_phone = forms.CharField(initial=faculty_profile.personal_phone)
#         guardian_phone = forms.CharField(initial=faculty_profile.guardian_phone)

#         class Meta:
#             model = CustomUser
#             fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

#     if request.method == 'POST':
#         form = EditFacultyForm(request.POST)
#         if form.is_valid():
#             user.first_name = form.cleaned_data['first_name']
#             user.last_name = form.cleaned_data['last_name']
#             user.email = form.cleaned_data['email']
#             user.username = form.cleaned_data['username']
#             user.set_password(form.cleaned_data['password1'])
#             user.save()

#             faculty_profile.department = form.cleaned_data['department']
#             faculty_profile.joining_date = form.cleaned_data['joining_date']
#             faculty_profile.personal_phone = form.cleaned_data['personal_phone']
#             faculty_profile.guardian_phone = form.cleaned_data['guardian_phone']
#             faculty_profile.save()

#             return redirect('admin_view_faculty')
#     else:
#         form = EditFacultyForm()

#     return render(request, 'attendance/admin_add_faculty.html', {'form': form})

from .forms import EditFacultyForm,AttendanceForm,AttendanceForm1

def admin_edit_faculty(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    faculty_profile = get_object_or_404(FacultyProfile, user=user)

    if request.method == 'POST':
        form = EditFacultyForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Update FacultyProfile manually
            faculty_profile.department = form.cleaned_data['department']
            faculty_profile.joining_date = form.cleaned_data['joining_date']
            faculty_profile.personal_phone = form.cleaned_data['personal_phone']
            faculty_profile.guardian_phone = form.cleaned_data['guardian_phone']
            faculty_profile.save()
            return redirect('admin_view_faculty')
    else:
        # Set initial data for both User and FacultyProfile fields
        initial_data = {
            'department': faculty_profile.department,
            'joining_date': faculty_profile.joining_date,
            'personal_phone': faculty_profile.personal_phone,
            'guardian_phone': faculty_profile.guardian_phone,
        }
        form = EditFacultyForm(instance=user, initial=initial_data)

    return render(request, 'attendance/admin_edit_faculty.html', {'form': form})


from django.db.models import Count, Q
from .models import Attendance, CustomUser

from calendar import monthrange
from datetime import date

# def attendance_summary(request):
#     faculty_users = CustomUser.objects.filter(is_faculty=True)
#     summary = []

#     today = date.today()
#     current_year = today.year
#     current_month = today.month

#     for faculty in faculty_users:
#         total_days = monthrange(current_year, current_month)[1]

#         present_days = Attendance.objects.filter(
#             faculty=faculty,
#             date__month=current_month,
#             date__year=current_year,
#             status='P'
#         ).count()

#         absent_days = Attendance.objects.filter(
#             faculty=faculty,
#             date__month=current_month,
#             date__year=current_year,
#             status='A'
#         ).count()

#         leave_days = Attendance.objects.filter(
#             faculty=faculty,
#             date__month=current_month,
#             date__year=current_year,
#             status='L'
#         ).count()

#         summary.append({
#             'faculty': faculty,
#             'present': present_days,
#             'absent': absent_days,
#             'leave': leave_days,
#             'total_days': total_days
#         })

#     return render(request, 'attendance/attendance_summary.html', {'summary': summary, 'month': current_month})
from calendar import monthrange
from datetime import date
from django.shortcuts import render
from .models import Attendance, CustomUser
from django.db.models import Q

from datetime import date
from django.db.models import Q
from django.shortcuts import render
from .models import Attendance, CustomUser

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # You may need to install python-dateutil

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from .models import Attendance, CustomUser

def attendance_summary(request):
    today = date.today()

    # Academic year: May 2025 to March 2026
    academic_start = date(2025, 5, 1)
    academic_end = date(2026, 3, 31)

    # Get selected month/year or default to current (only if within academic year)
    try:
        selected_month = int(request.GET.get('month', today.month))
        selected_year = int(request.GET.get('year', today.year))
    except ValueError:
        selected_month = today.month
        selected_year = today.year

    # If current date is outside academic year, default to May 2025
    if not (academic_start <= date(selected_year, selected_month, 1) <= academic_end):
        selected_month = 5
        selected_year = 2025

    faculty_users = CustomUser.objects.filter(is_faculty=True)

    # Search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        faculty_users = faculty_users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query)
        )

    summary = []
    for faculty in faculty_users:
        present_days = Attendance.objects.filter(
            faculty=faculty,
            date__month=selected_month,
            date__year=selected_year,
            status='P',
            approved=True
        ).count()

        absent_days = Attendance.objects.filter(
            faculty=faculty,
            date__month=selected_month,
            date__year=selected_year,
            status='A',
            approved=True
        ).count()

        leave_days = Attendance.objects.filter(
            faculty=faculty,
            date__month=selected_month,
            date__year=selected_year,
            status='L',
            approved=True
        ).count()

        attendance_records = Attendance.objects.filter(
            faculty=faculty,
            date__month=selected_month,
            date__year=selected_year,
            status='P',
            approved=True
        ).values('date', 'hours_worked')

        total_hours = 0
        daily_hours = []
        for record in attendance_records:
            hours = record['hours_worked'] or 0
            total_hours += hours
            daily_hours.append({
                'date': record['date'],
                'hours_worked': hours
            })
            

        summary.append({
            'faculty': faculty,
            'present': present_days,
            'absent': absent_days,
            'leave': leave_days,
            'total_hours': total_hours,
            'daily_hours': daily_hours
        })

    # Build dropdown months only from academic year range
    months = []
    current = academic_start
    while current <= academic_end:
        months.append({
            'month': current.month,
            'year': current.year,
            'label': current.strftime("%B %Y"),
            'value': f"{current.month}-{current.year}"
        })
        current += relativedelta(months=1)

    return render(request, 'attendance/attendance_summary.html', {
        'summary': summary,
        'month': datetime(selected_year, selected_month, 1).strftime("%B %Y"),
        'months': months,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'search_query': search_query
    })



from django.utils import timezone
from .models import Attendance
from django.contrib import messages
from decimal import Decimal, InvalidOperation

# @login_required
# def mark_attendance(request):
#     if request.method == 'POST':
#         user = request.user
#         today = timezone.now().date()
        
#         # Prevent duplicate marking
#         if Attendance.objects.filter(faculty=user, date=today).exists():
#             messages.warning(request, "Attendance already marked.")
#             return redirect('faculty_dashboard')

#         hours_worked = request.POST.get('hours_worked')
#         message = request.POST.get('message')

#         # Create attendance record
#         Attendance.objects.create(
#             faculty=user,
#             date=today,
#             status='P',
#             approved=False,
#             hours_worked=hours_worked,
#             message=message
#         )
#         messages.success(request, "Attendance marked successfully.")
#         return redirect('faculty_dashboard')

#     return redirect('faculty_dashboard')


# @login_required
# def mark_attendance(request):
#     if request.method == 'POST':
#         user = request.user
#         today = timezone.now().date()

#         # Prevent duplicate marking
#         if Attendance.objects.filter(faculty=user, date=today).exists():
#             messages.warning(request, "Attendance already marked.")
#             return redirect('faculty_dashboard')

#         try:
#             hours_worked = Decimal(request.POST.get('hours_worked'))
#         except (TypeError, InvalidOperation):
#             messages.error(request, "Invalid number of hours.")
#             return redirect('faculty_dashboard')

#         message = request.POST.get('message', '')

#         Attendance.objects.create(
#             faculty=user,
#             date=today,
#             status='P',
#             approved=False,
#             hours_worked=hours_worked,
#             message=message
#         )

#         messages.success(request, "Attendance marked successfully.")
#         return redirect('faculty_dashboard')

#     return redirect('faculty_dashboard')

@login_required
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('admin_approve_attendance')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/edit_attendance.html', {'form': form, 'attendance': attendance})

@login_required
def edit_attendance1(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('admin_view_attendance')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/edit_attendance1.html', {'form': form, 'attendance': attendance})

@login_required
def edit_attendance2(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        form = AttendanceForm1(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('faculty_attendance_history')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/edit_attendance2.html', {'form': form, 'attendance': attendance})

@login_required
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('faculty_attendance_history')

    return render(request, 'attendance/confirm_delete_attendance.html', {'attendance': attendance})
@login_required
def delete_attendance1(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('admin_view_attendance')

    return render(request, 'attendance/confirm_delete_attendance1.html', {'attendance': attendance})

@login_required
def delete_attendance2(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('admin_approve_attendance')

    return render(request, 'attendance/confirm_delete_attendance2.html', {'attendance': attendance})

@login_required
def mark_attendance_page(request):
    today = date.today()
    attendance_exists = Attendance.objects.filter(faculty=request.user, date=today).exists()

    return render(request, 'attendance/mark_attendance_page.html', {
        'today': today,
        'attendance_exists': attendance_exists
    })


# @login_required
# def mark_attendance(request):
#     if request.method == 'POST':
#         today = date.today()

#         # Prevent duplicate entries
#         if Attendance.objects.filter(faculty=request.user, date=today).exists():
#             messages.warning(request, "You have already marked attendance for today.")
#             return redirect('mark_attendance_page')

#         hours_worked = request.POST.get('hours_worked')
#         message = request.POST.get('message', '')

#         Attendance.objects.create(
#             faculty=request.user,
#             date=today,
#             status='P',  # You can make this dynamic if needed
#             hours_worked=hours_worked,
#             message=message
#         )
#         messages.success(request, "✅ Attendance marked successfully!")
#         return redirect('faculty_dashboard')

#     return redirect('mark_attendance_page')

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        today = date.today()

        if Attendance.objects.filter(faculty=request.user, date=today).exists():
            messages.warning(request, "You have already marked attendance for today.")
            return redirect('mark_attendance_page')

        hours_worked = request.POST.get('hours_worked')
        message = request.POST.get('message', '')

        Attendance.objects.create(
            faculty=request.user,
            date=today,
            status='P',
            hours_worked=hours_worked,
            message=message
        )
        messages.success(request, "✅ Attendance marked successfully!")
        return redirect('faculty_dashboard')

    # Optional: Instead of redirecting back and looping,
    # show a 405 Method Not Allowed
    return HttpResponseNotAllowed(['POST'])

def admin_view_faculty_detail(request, faculty_id):
    faculty = get_object_or_404(CustomUser, id=faculty_id, is_faculty=True)
    return render(request, 'attendance/admin_faculty_detail.html', {'faculty': faculty})


from django.shortcuts import get_object_or_404

def view_attendance_detail(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    return render(request, 'attendance/view_attendance_detail.html', {'attendance': attendance})

from django.core.management import call_command
from django.http import HttpResponse


def migrate_view(request):
    call_command('migrate')
    return HttpResponse("Migration completed.")

# from django.http import HttpResponse
# from django.contrib.auth.models import User

# def create_superuser(request):
#     if User.objects.filter(username='admin').exists():
#         return HttpResponse("Superuser already exists.")
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
#     return HttpResponse("Superuser created. Username: admin, Password: admin123")

from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(request):
    if User.objects.filter(username='admin').exists():
        return HttpResponse("Superuser already exists.")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    return HttpResponse("Superuser created. Username: admin, Password: admin123")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.management import call_command

@csrf_exempt
def run_auto_mark_absent(request):
    if request.method == "POST":
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token == settings.SECRET_JOB_TOKEN:
            try:
                call_command("auto_mark_absent")
                return JsonResponse({"status": "success"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "unauthorized"}, status=403)


# from django.http import JsonResponse
# import os

# def run_job(request):
#     token = request.headers.get("Authorization")
#     expected_token = f"Bearer {os.getenv('SECRET_JOB_TOKEN', 'change-this-token')}"

#     if token != expected_token:
#         return JsonResponse({"error": "Unauthorized"}, status=401)

#     from django.core.management import call_command
#     call_command("auto_mark_absent")

#     return JsonResponse({"status": "Job executed successfully"})

from django.http import JsonResponse
import os

# @csrf_exempt
# def run_job(request):
#     token = request.headers.get("Authorization")
#     expected_token = f"Bearer {os.getenv('SECRET_JOB_TOKEN', 'change-this-token')}"

#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid method", "method": request.method}, status=405)

#     if token != expected_token:
#         return JsonResponse({"error": "Unauthorized", "received_token": token}, status=401)

#     from django.core.management import call_command
#     call_command("auto_mark_absent")

#     return JsonResponse({"status": "Job executed successfully"})
@csrf_exempt
def run_job(request):
    token = request.headers.get("Authorization")
    expected_token = f"Bearer {os.getenv('SECRET_JOB_TOKEN', 'change-this-token')}"
    
    print("Received token:", token)
    print("Expected token:", expected_token)

    if request.method != "POST":
        return JsonResponse({"error": "Invalid method", "method": request.method}, status=405)

    if token != expected_token:
        return JsonResponse({"error": "Unauthorized", "received_token": token}, status=401)

    from django.core.management import call_command
    call_command("auto_mark_absent")

    return JsonResponse({"status": "Job executed successfully"})

# @csrf_exempt
# def run_job(request):
#     token = request.headers.get("Authorization")
#     expected_token = f"Bearer {os.getenv('SECRET_JOB_TOKEN', 'change-this-token')}"

#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid method"}, status=405)

#     if token != expected_token:
#         return JsonResponse({"error": "Unauthorized"}, status=401)

#     # Just a ping to keep app alive
#     return JsonResponse({"status": "App is awake"})

