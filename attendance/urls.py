from django.urls import path
from . import views
from .views import run_job

urlpatterns = [
    path('', views.home, name='home'),  # 👈 Home page
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/mark/', views.mark_attendance, name='mark_attendance'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-view-faculty/', views.admin_view_faculty, name='admin_view_faculty'),
    path('admin-view-attendance/', views.admin_view_attendance, name='admin_view_attendance'),
    path('admin-add-faculty/', views.admin_add_faculty, name='admin_add_faculty'),
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard')
    path('logout/', views.custom_logout, name='logout'),
    path('admin-approve-attendance/', views.admin_approve_attendance, name='admin_approve_attendance'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty-attendance-history/', views.faculty_attendance_history, name='faculty_attendance_history'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('faculty/edit/<int:user_id>/', views.admin_edit_faculty, name='admin_edit_faculty'),
    path('faculty/delete/<int:user_id>/', views.admin_delete_faculty, name='admin_delete_faculty'),
    path('attendance-summary/', views.attendance_summary, name='attendance_summary'),

    path('attendance-summary/pdf/', views.attendance_summary_pdf, name='attendance_summary_pdf'),
    path('attendance-summary/excel/', views.attendance_summary_excel, name='attendance_summary_excel'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('mark-leave-page/', views.mark_leave_page, name='mark_leave_page'),
    path('mark-leave/', views.mark_leave, name='mark_leave'),
    # path('admin/edit_attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    # path('admin/delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('edit_attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    path('delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('delete_attendance1/<int:attendance_id>/', views.delete_attendance1, name='delete_attendance1'),
    path('delete_attendance2/<int:attendance_id>/', views.delete_attendance2, name='delete_attendance2'),
    path('attendance/view/<int:attendance_id>/', views.view_attendance, name='view_attendance'),

    path('edit_attendance1/<int:attendance_id>/', views.edit_attendance1, name='edit_attendance1'),
    path('edit_attendance2/<int:attendance_id>/', views.edit_attendance2, name='edit_attendance2'),
   
    path('faculty/submit/', views.mark_attendance, name='mark_attendance'),
    path('faculty/mark-page/', views.mark_attendance_page, name='mark_attendance_page'),
    # urls.py
    # path('admin/faculty/<int:faculty_id>/view/', views.admin_view_faculty_detail, name='admin_view_faculty_detail'),
    path('faculty/<int:faculty_id>/view/', views.admin_view_faculty_detail, name='admin_view_faculty_detail'),
    path('attendance/<int:attendance_id>/view/', views.view_attendance_detail, name='view_attendance_detail'),
    path('run-migrations/', views.migrate_view),
    path('create-superuser/', views.create_superuser),
    path("run-job/", run_job),







]
