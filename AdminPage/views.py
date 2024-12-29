from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from ElementaryEnrollment.models import Student, User, Father, Mother
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST 
from django.core.paginator import Paginator 


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_view_student_records(request):
    return render(request, 'admin_view_student_records.html')

def admin_set_enrollment_period(request):
    return render(request, 'admin_set_enrollment_period.html')

def admin_approved_rejected_History(request):
    return render(request, 'admin_approved_rejected_History.html')

def admin_deleted_accounts_history(request):
    return render(request, 'admin_deleted_accounts_history.html')



def add_registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('admin_manage_accounts')

        # If username is unique, proceed to create the user and registrar account
        if username and password:
            user = User(username=username, password=make_password(password))
            user.save()
            
            # Create an entry in the Registrar table with the user id
            Registrar.objects.create(user_id=user.id)  # Save to Registrar table
            
            messages.success(request, "Registrar account created successfully.")
            return redirect('admin_manage_accounts')

    return render(request, 'admin_manage_accounts.html')

def get_student_details(request, student_id):
    student = Student.objects.get(id=student_id)
    requirements = Requirement.objects.filter(student=student)
    
    # Construct response data
    data = {
        'name': f"{student.first_name} {student.last_name}",
        'grade_level': student.grade_level,
        'status': student.status,
        'requirements': ", ".join([req.document_name for req in requirements])  # Example field
    }
    return JsonResponse(data)

def manage_accounts(request):
    pending_students = Student.objects.filter(status='Pending')
    return render(request, 'manage_accounts.html', {'students': pending_students})

def approve_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.status = 'Approved'
    student.save()
    AccountHistory.objects.create(student=student, action='Approved')
    return redirect('manage_accounts')

def reject_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.status = 'Rejected'
    student.save()
    AccountHistory.objects.create(student=student, action='Rejected')
    return redirect('manage_accounts')

def history(request):
    history_records = AccountHistory.objects.all()
    return render(request, 'history.html', {'history_records': history_records})



# Main Functional Views
def admin_manage_accounts(request):
    # Fetch only pending accounts
    accounts = Student.objects.filter(status='Pending')  # Filter only Pending

    # Handle sorting and searching
    sort_by = request.GET.get('sort', 'date')
    search_query = request.GET.get('search', '')

    if sort_by == 'name':
        accounts = accounts.order_by('last_name', 'first_name')
    elif sort_by == 'date':
        accounts = accounts.order_by('date_joined')

    if search_query:
        accounts = accounts.filter(last_name__icontains=search_query) | accounts.filter(first_name__icontains=search_query)
    
    return render(request, 'admin_manage_accounts.html', {'accounts': accounts})

def approve_account(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.status = 'Regular'
    student.save()  # `save` method will generate `student_id` if needed
    messages.success(request, "Student account approved and Student ID generated.")
    return redirect('admin_manage_accounts')

def reject_account(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.status  = 'Rejected'
    ArchivedAccount.objects.create(student=student)  # Archive rejected accounts
    messages.success(request, "Student account rejected and archived.")
    return redirect('admin_manage_accounts')

def add_registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Directly create the user without additional validation for testing purposes
            user = User.objects.create(username=username, password=make_password(password))
            user.save()  # Ensure saving to the database
            messages.success(request, "Registrar account created successfully.")
            return redirect('admin_manage_accounts')

    return render(request, 'admin_manage_accounts.html')

def view_registration_form(request, student_id):
    # Fetch student data
    student = get_object_or_404(Student, id=student_id)
    mother = Mother.objects.filter(student=student).first()
    father = Father.objects.filter(student=student).first()
    
    # Prepare data to pass to the template
    student_data = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'middle_name': student.middle_name,
        'last_name': student.last_name,
        'birth_date': student.birth_date,
        'sex': student.sex,
        'email': student.email,
        'street': student.street,
        'barangay': student.barangay,
        'city': student.city,
        'state_province': student.state_province,
        'country': student.country,
    }

    mother_data = {
        'first_name': mother.first_name if mother else '',
        'middle_name': mother.middle_name if mother else '',
        'last_name': mother.last_name if mother else '',
        'birth_date': mother.birth_date if mother else '',
        'occupation': mother.occupation if mother else '',
        'contact': mother.contact if mother else '',
        'street': mother.street if mother else '',
        'barangay': mother.barangay if mother else '',
        'city': mother.city if mother else '',
        'state_province': mother.state_province if mother else '',
        'country': mother.country if mother else '',
    }

    father_data = {
        'first_name': father.first_name if father else '',
        'middle_name': father.middle_name if father else '',
        'last_name': father.last_name if father else '',
        'birth_date': father.birth_date if father else '',
        'occupation': father.occupation if father else '',
        'contact': father.contact if father else '',
        'street': father.street if father else '',
        'barangay': father.barangay if father else '',
        'city': father.city if father else '',
        'state_province': father.state_province if father else '',
        'country': father.country if father else '',
    }

    # Render the template with the data
    return render(request, 'View_Registration_Form.html', {
        'student_data': student_data,
        'mother_data': mother_data,
        'father_data': father_data,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            student = Student.objects.filter(user=user).first()
            
            if student:
                if student.first_login:
                    auth_login(request, user)
                    return redirect('enrollment_form_view')  # Redirects first-time login to enrollment
                else:
                    auth_login(request, user)
                    return redirect('student_dashboard')
            else:
                messages.error(request, "No student record linked to this user.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'LOGIN.html')



@csrf_exempt
@require_POST
def update_grade_level(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    new_grade_level = request.POST.get('grade_level')

    if new_grade_level:
        student.grade_level = new_grade_level
        student.save()  # Save the grade level directly to the database
        return JsonResponse({'success': True, 'message': 'Grade level updated successfully.'})
    
    return JsonResponse({'success': False, 'message': 'Failed to update grade level.'})

@csrf_exempt
@require_POST
def assign_section(request, student_id):
    sections = ["Section A", "Section B", "Section C", "Section D", "Section E"]
    selected_section = random.choice(sections)
    
    student = get_object_or_404(Student, id=student_id)
    student.section = selected_section
    student.save()  # Save the section directly to the database
    return JsonResponse({'success': True, 'section': selected_section})

@login_required
def accept_enrollment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if student.grade_level and student.section:
        student.enrollment_status = 'Regular'
        student.save()
        messages.success(request, f"{student.first_name} {student.last_name}'s enrollment has been approved.")
    else:
        messages.error(request, "Please set both grade level and section before approving.")
    
    return redirect('manage_enrollees')

def registrar_rejected_forms(request):
    # Fetch students whose enrollment status is 'Rejected'
    rejected_forms = Student.objects.filter(enrollment_status='Rejected')
    return render(request, 'Registrar_rejected_forms.html', {'rejected_forms': rejected_forms})




@login_required
def accept_enrollment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.enrollment_status = 'Approved'
    student.save()
    messages.success(request, f"{student.first_name} {student.last_name}'s enrollment has been approved.")
    return redirect('manage_enrollees')

@login_required
def reject_enrollment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.enrollment_status = 'Rejected'
    student.save()
    messages.error(request, f"{student.student_first_name} {student.student_last_name}'s enrollment has been rejected.")
    return redirect('manage_enrollees')




def manage_enrollees(request):
    # Get filter criteria from the request
    grade_level = request.GET.get('grade_level')
    search_query = request.GET.get('search_query')
    
    # Filter enrollees with 'Pending Enrollment' status
    enrollees = Student.objects.filter(enrollment_status='Pending Enrollment')  # Assuming Student is filtered here
    
    # Additional filters for grade level and search query
    if grade_level and grade_level != "All Grades":
        enrollees = enrollees.filter(enrollment__grade_level=grade_level)
    if search_query:
        enrollees = enrollees.filter(last_name__icontains=search_query)
    
    # Define grades list for dropdown in the template
    grades = list(range(1, 7))  # [1, 2, 3, 4, 5, 6]

    context = {
        'enrollees': enrollees,
        'grades': grades,
        'grade_level': grade_level,
        'search_query': search_query,
    }
    return render(request, 'Registrar_manage_enrollees.html', context)


def view_enrollment_form(request, student_id):
    # Retrieve the student instance and related enrollment, mother, and father information
    student = get_object_or_404(Student, id=student_id)
    enrollment = Enrollment.objects.filter(student=student).first()
    mother = Mother.objects.filter(student=student).first()
    father = Father.objects.filter(student=student).first()

    context = {
        'student': student,
        'enrollment': enrollment,
        'mother': mother,
        'father': father
    }
    
    return render(request, 'view_enrollment_form.html', context)


def registrar_enrolled_students(request):
    # Fetch all approved enrolled students
    approved_students = Student.objects.filter(enrollment_status='Approved')
    
    # Pagination setup
    paginator = Paginator(approved_students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Registrar_enrolled_students.html', {'page_obj': page_obj})




def view_detailed_student_info(request, student_id):
    # Retrieve student instance and related information
    student = get_object_or_404(Student, id=student_id)
    enrollment = Enrollment.objects.filter(student=student).first()
    mother = Mother.objects.filter(student=student).first()
    father = Father.objects.filter(student=student).first()

    # Prepare student data for the template, covering each attribute in models
    student_data = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'middle_name': student.middle_name,
        'last_name': student.last_name,
        'birth_date': student.birth_date,
        'sex': student.sex,
        'email': student.email,
        'address': f"{student.street}, {student.barangay}, {student.city}, {student.state_province}, {student.country}",
        'grade_level': enrollment.grade_level if enrollment else None,
        'section': enrollment.class_section if enrollment and hasattr(enrollment, 'class_section') else None,  # Updated line
    }

    mother_data = {
        'first_name': mother.first_name if mother else '',
        'middle_name': mother.middle_name if mother else '',
        'last_name': mother.last_name if mother else '',
        'birth_date': mother.birth_date if mother else '',
        'occupation': mother.occupation if mother else '',
        'contact': mother.contact if mother else '',
        'address': f"{mother.street}, {mother.barangay}, {mother.city}, {mother.state_province}, {mother.country}" if mother else '',
    }

    father_data = {
        'first_name': father.first_name if father else '',
        'middle_name': father.middle_name if father else '',
        'last_name': father.last_name if father else '',
        'birth_date': father.birth_date if father else '',
        'occupation': father.occupation if father else '',
        'contact': father.contact if father else '',
        'address': f"{father.street}, {father.barangay}, {father.city}, {father.state_province}, {father.country}" if father else '',
    }

    context = {
        'student_data': student_data,
        'mother_data': mother_data,
        'father_data': father_data
    }

    return render(request, 'view_detailed_student_info.html', context)




def student_schedule(request):
    return render(request, 'Student_Schedule.html')
