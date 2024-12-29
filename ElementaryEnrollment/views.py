from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import StudentForm, MotherForm, FatherForm, DocumentForm, CreateAccountForm, EnrollmentFormNewStudent, EnrollmentFormTransferee
from .models import Student, Mother, Father, ArchivedAccount
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Student, Enrollment, Schedule  # Assuming these models exist and are relevant
from django.utils import timezone
from .models import Enrollment
from .forms import StudentEditForm
from django.views.decorators.http import require_POST
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@login_required
def student_profile(request):
    try:
        # Retrieve the Student record based on the logged-in user
        student = Student.objects.get(user=request.user)

        # Prepare the student data for the template
        student_data = {
            "id": student.id,  # Add the student ID here
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.middle_name or ''} {student.last_name}",
            "birth_date": student.birth_date,
            "sex": student.sex,
            "email": student.email,
            "address": f"{student.street}, {student.barangay}, {student.city}, {student.state_province}, {student.country}",
        }
    except Student.DoesNotExist:
        # If no Student record is found for the user, set an error message
        student_data = {"error": "No student record found for this user."}

    # Render the profile template with the student data
    return render(request, 'Student_Profile.html', {"student_data": student_data})


def enrollment_form_view(request):

    # Define the forms for initial loading or error cases
    form_new = EnrollmentFormNewStudent()
    form_transferee = EnrollmentFormTransferee()

    if request.method == 'POST':
        print("POST Data:", request.POST)
        student_type = request.POST.get('student_type')

        # Conditional handling based on student_type
        if student_type == "new":
            form = EnrollmentFormNewStudent(request.POST, request.FILES)
        elif student_type == "transfer":
            form = EnrollmentFormTransferee(request.POST, request.FILES)
        else:
            messages.error(request, "Invalid student type selected.")
            return render(request, 'ENROLLMENT_FORM.html', {'form_new': form_new, 'form_transferee': form_transferee})

        if form.is_valid():
            # For testing, confirm form data saved
            enrollment = form.save(commit=False)

            messages.success(request, "Enrollment form submitted successfully.")
            return redirect('student_dashboard')
        else:
            print("Form errors:", form.errors)  # Log form errors for debugging
            messages.error(request, "There was an issue with your submission. Please check your data.")

    return render(request, 'ENROLLMENT_FORM.html', {
        'form_new': form_new,
        'form_transferee': form_transferee
    })


# Registration Views
def registration_view(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        mother_form = MotherForm(request.POST, prefix='mother')
        father_form = FatherForm(request.POST, prefix='father')
        document_form = DocumentForm(request.POST, request.FILES)

        if student_form.is_valid() and mother_form.is_valid() and father_form.is_valid() and document_form.is_valid():
            # Convert date fields to strings for session storage
            student_data = student_form.cleaned_data
            student_data['birth_date'] = student_data['birth_date'].strftime('%Y-%m-%d')  # Convert to string

            mother_data = mother_form.cleaned_data
            mother_data['birth_date'] = mother_data['birth_date'].strftime('%Y-%m-%d')  # Convert to string

            father_data = father_form.cleaned_data
            father_data['birth_date'] = father_data['birth_date'].strftime('%Y-%m-%d')  # Convert to string

            # Store the data in session
            request.session['student_data'] = student_data
            request.session['mother_data'] = mother_data
            request.session['father_data'] = father_data

            return redirect('review')
    else:
        student_form = StudentForm()
        mother_form = MotherForm(prefix='mother')
        father_form = FatherForm(prefix='father')
        document_form = DocumentForm()

    return render(request, 'REGISTRATION_FORM.html', {
        'student_form': student_form,
        'mother_form': mother_form,
        'father_form': father_form,
        'document_form': document_form
    })

def review(request):
    # Retrieve session data
    student_data = request.session.get('student_data')
    mother_data = request.session.get('mother_data')
    father_data = request.session.get('father_data')

    if not student_data or not mother_data or not father_data:
        return redirect('registration')

    if request.method == 'POST':
        if 'confirm' in request.POST:
            # Save data to the database upon confirmation
            student = Student.objects.create(
                **student_data,
                status ='Pending'  # Set default approval status to Pending
            )
            Mother.objects.create(student=student, **mother_data)
            Father.objects.create(student=student, **father_data)

            # Store the new student's ID in the session for later use
            request.session['student_id'] = student.id
            
            # Clear session data
            request.session.pop('student_data')
            request.session.pop('mother_data')
            request.session.pop('father_data')
            
            return redirect('create_account')
        elif 'back' in request.POST:
            return redirect('registration')

    return render(request, 'REVIEW.html', {
        'student_data': student_data,
        'mother_data': mother_data,
        'father_data': father_data
    })

def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Create the User
            user = User.objects.create(username=username, password=make_password(password))

            # Retrieve the Student instance using the session 'student_id'
            student_id = request.session.get('student_id')
            if student_id:
                student = Student.objects.get(id=student_id)
                student.user = user  # Link the User to the Student
                student.save()

                # Clear the session after linking
                request.session.pop('student_id', None)
                messages.success(request, "Account created successfully. Please wait for admin approval.")
                return redirect('login')
            else:
                messages.error(request, "Student ID not found in session. Please retry registration.")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = CreateAccountForm()

    return render(request, 'create_account.html', {'form': form})

# Additional Views
def enrollment_confirmation(request):
    return render(request, 'Email Confirmation.html')

def student_dashboard(request):
    return render(request, 'Student_Dashboard.html')

def student_schedule(request):
    return render(request, 'Student_Schedule.html')

from django.utils import timezone

@login_required
def student_status(request):
    student = Student.objects.get(user=request.user)
    enrollment = Enrollment.objects.filter(student=student).first()
    
    # Calculate Passed Grades
    if enrollment.student_type == 'new':
        passed_grades = "Grade 1"
    elif enrollment.student_type == 'transfer':
        passed_grades = "Waiting For Evaluation"
    else:
        passed_grades = "N/A"
    
    # Determine current school year
    current_year = timezone.now().year
    school_year = f"{current_year}-{current_year + 1}"
    
    # Determine Status
    status = student.enrollment_status  # This assumes enrollment status tracks pending/approved/rejected

    context = {
        'passed_grades': passed_grades,
        'school_year': school_year,
        'status': status,
    }

    return render(request, 'Student_Status.html', context)


def student_requirements(request):
    return render(request, 'Student_Requirements.html')

def reset_password(request):
    return render(request, 'Reset Password.html')

def forgot_password(request):
    return render(request, 'Forgot Password.html')

def student_account(request):
    return render(request, 'Student_Account.html')

def logout_view(request):
    return render (request, 'LOGIN.html')


def edit_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('student_profile')  # Redirect to the profile page after editing
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'Edit_Profile.html', {'form': form, 'student': student})

#ADMIN---------------------------------------------------------------------------------------

#REGISTRAR------------------------------------------------------------------------
