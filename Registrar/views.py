from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from ElementaryEnrollment.models import Student, Enrollment, Schedule   
import random




def registrar_dashboard(request):
    # Any required data for the dashboard can be fetched here
    return render(request, 'Registrar_dashboard.html')




def get_student_info(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        enrollment = student.enrollment_set.first()  # Assumes one enrollment record per student
        
        # Build requirements links if they exist
        requirements = ""
        if enrollment:
            if enrollment.kindergarten_certificate:
                requirements += f'<a href="{enrollment.kindergarten_certificate.url}" target="_blank">Kindergarten Certificate</a><br>'
            if enrollment.transferee_report_card:
                requirements += f'<a href="{enrollment.transferee_report_card.url}" target="_blank">Transferee Report Card</a><br>'
        
        # Collect guardian information if available
        mother_info = None
        father_info = None
        if hasattr(student, 'mother'):
            mother = student.mother
            mother_info = {
                'name': f"{mother.first_name} {mother.last_name}",
                'contact': mother.contact,
                'occupation': mother.occupation,
                'birth_date': mother.birth_date,
                'address': f"{mother.street}, {mother.barangay}, {mother.city}, {mother.state_province}, {mother.country}",
            }
        if hasattr(student, 'father'):
            father = student.father
            father_info = {
                'name': f"{father.first_name} {father.last_name}",
                'contact': father.contact,
                'occupation': father.occupation,
                'birth_date': father.birth_date,
                'address': f"{father.street}, {father.barangay}, {father.city}, {father.state_province}, {father.country}",
            }
        
        # Collect uploaded documents if any
        documents = [
            {'file_name': doc.file_uploaded.name, 'url': doc.file_uploaded.url}
            for doc in student.documents.all()
        ]

        # Compile all student data
        student_info = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'birth_date': student.birth_date,
            'email': student.email,
            'address': f"{student.street}, {student.barangay}, {student.city}, {student.state_province}, {student.country}",
            'grade_level': student.grade_level or 'N/A',
            'section': student.section or 'N/A',
            'enrollment_status': student.enrollment_status or 'N/A',
            'requirements': requirements if requirements else "No requirements uploaded",
            'mother_info': mother_info,
            'father_info': father_info,
            'documents': documents,
        }
        return JsonResponse(student_info)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)



def registrar_schedule(request):
    time_intervals = [
        '7:00 AM - 8:00 AM',
        '8:00 AM - 9:00 AM',
        '9:00 AM - 10:00 AM',
        '10:00 AM - 11:00 AM',
        '11:00 AM - 12:00 PM'
    ]
    subjects = ['Math', 'Science', 'English', 'History', 'Physical Education']
    retrieved_schedule = {}

    # Get already assigned grade levels and sections, format as "grade-section" for JavaScript use
    existing_schedules = Schedule.objects.values('grade_level', 'section').distinct()
    excluded_grade_sections = [f"{entry['grade_level']}-{entry['section']}" for entry in existing_schedules]

    if request.method == 'POST':
        grade_level = request.POST.get('grade_level')
        section = request.POST.get('section')
        
        if not grade_level or not section:
            messages.error(request, "Grade level and section are required.")
            return render(request, 'Registrar_schedule.html', {
                'time_intervals': enumerate(time_intervals),
                'subjects': subjects,
                'excluded_grade_sections': excluded_grade_sections,
            })

        action = request.POST.get('action')
        
        if action == 'set_random':
            for idx, time_slot in enumerate(time_intervals):
                random.shuffle(subjects)
                schedule_data = {
                    'grade_level': grade_level,
                    'section': section,
                    'time_slot': time_slot,
                    'mon_7': subjects[0],
                    'tue_7': subjects[1],
                    'wed_7': subjects[2],
                    'thu_7': subjects[3],
                    'fri_7': subjects[4]
                }
                Schedule.objects.update_or_create(
                    grade_level=grade_level, section=section, time_slot=time_slot,
                    defaults=schedule_data
                )
            messages.success(request, "Schedule set with unique random subjects for each day successfully.")
            return redirect('registrar_schedule')
        
        # Save the schedule entries manually if not random
        for idx, time_slot in enumerate(time_intervals):
            schedule_data = {
                'grade_level': grade_level,
                'section': section,
                'time_slot': time_slot,
                'mon_7': request.POST.get(f'mon_{idx}'),
                'tue_7': request.POST.get(f'tue_{idx}'),
                'wed_7': request.POST.get(f'wed_{idx}'),
                'thu_7': request.POST.get(f'thu_{idx}'),
                'fri_7': request.POST.get(f'fri_{idx}')
            }
            Schedule.objects.create(**schedule_data)
        messages.success(request, "Schedule saved successfully.")
        return redirect('registrar_schedule')

    elif request.method == 'GET' and 'grade_level' in request.GET and 'section' in request.GET:
        action = request.GET.get('action')
        grade_level = request.GET.get('grade_level')
        section = request.GET.get('section')

        if action == 'retrieve':
            schedule_entries = Schedule.objects.filter(grade_level=grade_level, section=section)
            for entry in schedule_entries:
                retrieved_schedule[entry.time_slot] = {
                    'mon': entry.mon_7,
                    'tue': entry.tue_7,
                    'wed': entry.wed_7,
                    'thu': entry.thu_7,
                    'fri': entry.fri_7,
                }
            messages.info(request, "Schedule retrieved successfully.")
        
        elif action == 'delete':
            Schedule.objects.filter(grade_level=grade_level, section=section).delete()
            messages.success(request, "Schedule deleted successfully.")
            return redirect('registrar_schedule')

    return render(request, 'Registrar_schedule.html', {
        'time_intervals': enumerate(time_intervals),
        'subjects': subjects,
        'retrieved_schedule': retrieved_schedule,
        'excluded_grade_sections': excluded_grade_sections,
    })


def registrar_student_sections(request):
    # Display students by sections and grade levels (paginated if needed)
    grade_sections = {
        # This would ideally come from the database and include students in sections
        1: {'A': [], 'B': []},  # Example data structure for sections
        2: {'A': [], 'B': []},
    }
    return render(request, 'Registrar_student_sections.html', {'grade_sections': grade_sections})

def registrar_view_document(request, student_id):
    # Fetch student enrollment form data
    student = get_object_or_404(Student, id=student_id)
    enrollment = Enrollment.objects.filter(student=student).first()
    return render(request, 'Registrar_view_document.html', {'student': student, 'enrollment': enrollment})

def registrar_account(request):
    # Render account information or settings
    return render(request, 'Registrar_account.html')




