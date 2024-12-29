from django.urls import path 
from AdminPage import views



urlpatterns = [ 
    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('view-student-records/', views.admin_view_student_records, name='admin_view_student_records'),
    path('set-enrollment-period/', views.admin_set_enrollment_period, name='admin_set_enrollment_period'),
    path('approved-rejected-History/', views.admin_approved_rejected_History, name='admin_approved_rejected_History'),
    path('deleted-accounts-history/', views.admin_deleted_accounts_history, name='admin_deleted_accounts_history'),
    path('admin_manage_accounts/', views.admin_manage_accounts, name='admin_manage_accounts'),
    path('update_grade_level/<int:student_id>/', views.update_grade_level, name='update_grade_level'),
    path('manage_enrollees/', views.manage_enrollees, name='manage_enrollees'),
    path('update_grade_level/<int:student_id>/', views.update_grade_level, name='update_grade_level'),
    path('assign_section/<int:student_id>/', views.assign_section, name='assign_section'),
    path('view_enrollment_form/<int:student_id>/', views.view_enrollment_form, name='view_enrollment_form'),
    path('accept_enrollment/<int:student_id>/', views.accept_enrollment, name='accept_enrollment'),
    path('reject_enrollment/<int:student_id>/', views.reject_enrollment, name='reject_enrollment'),
    path('student/<int:student_id>/', views.view_registration_form, name='view_registration_form'),
    path('enrolled-students/', views.registrar_enrolled_students, name='registrar_enrolled_students'),
    path('student/<int:student_id>/', views.view_registration_form, name='view_registration_form'),
    path('student/info/<int:student_id>/', views.view_detailed_student_info, name='view_detailed_student_info'),
     path('save_schedule/', views.student_schedule, name='save_schedule'),  # Update to use student_schedule
     ]
     