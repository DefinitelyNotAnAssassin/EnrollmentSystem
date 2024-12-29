from django.urls import path
from ElementaryEnrollment import views 
from AdminPage import views as admin_views 
from Registrar import views as registrar_views   
urlpatterns = [
    path('register/', views.registration_view, name='registration'),
    path('enrollment_confirmation/', views.enrollment_confirmation, name='enrollment_confirmation'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('schedule/', views.student_schedule, name='student_schedule'),
    path('status/', views.student_status, name='student_status'),
    path('requirements/', views.student_requirements, name='student_requirements'),
    path('login/', admin_views.login_view, name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('Enrollment-Form/',views.enrollment_form_view, name='enrollment_form_view'),
    path('review/', views.review, name='review'),
    path('account/', views.student_account, name='student_account'),
    path('', views.enrollment_form_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('create_account/', views.create_account, name='create_account'),
    path('approve_account/<int:student_id>/', admin_views.approve_account, name='approve_account'),
    path('reject_account/<int:student_id>/', admin_views.reject_account, name='reject_account'),
    path('add_registrar/', admin_views.add_registrar, name='add_registrar'),
    path('view_registration_form/<int:student_id>/', admin_views.view_registration_form, name='view_registration_form'),
    path('profile/edit/<int:student_id>/', views.edit_profile, name='edit_profile'),

   
    
]
