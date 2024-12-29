from django.urls import path 
from Registrar import views
from AdminPage import views as admin_views 

urlpatterns = [
    path('registrar_dashboard/', views.registrar_dashboard, name='registrar_dashboard'),
    path('get_student_info/<int:student_id>/', views.get_student_info, name='get_student_info'),
    path('enrolled_students/', admin_views.registrar_enrolled_students, name='enrolled_students'),
    path('manage_enrollees/', admin_views.manage_enrollees, name='manage_enrollees'),
    path('rejected_forms/', admin_views.registrar_rejected_forms, name='rejected_forms'),
    path('registrar_schedule/', views.registrar_schedule, name='registrar_schedule'),
    path('student_sections/', views.registrar_student_sections, name='student_sections'),
    path('view_document/<int:student_id>/', views.registrar_view_document, name='view_document'),
    path('registrar_account/', views.registrar_account, name='registrar_account'),
    path('accept_enrollment/<int:student_id>/', admin_views.accept_enrollment, name='accept_enrollment'),
    path('reject_enrollment/<int:student_id>/', admin_views.reject_enrollment, name='reject_enrollment'),
    path('view-enrollment-form/<int:enrollee_id>/', admin_views.view_enrollment_form, name='view_enrollment_form'),
]
