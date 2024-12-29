# models.py
from django.db import models
from django.contrib.auth.models import User
import datetime

class Student(models.Model):
    student_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    suffix = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    email = models.EmailField()
    date_joined = models.DateField(auto_now_add=True)

    # Student address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    grade_level = models.IntegerField(null=True, blank=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True, blank=True)
    # Track initial login and enrollment status
    first_login = models.BooleanField(default=True)  # True if first login
    enrollment_status = models.CharField(
        max_length=24,  # Adjusted to match the longest choice
        choices=[
            ('Pending Account Creation', 'Pending Account Creation'),
            ('Pending Enrollment', 'Pending Enrollment'),
            ('Enrolled', 'Enrolled')
        ],
        default='Pending Account Creation'
    )

    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Regular'), ('Rejected', 'Rejected')], default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):  
        return f"{self.last_name}, {self.first_name} {self.middle_name} {self.student_id}"

    def save(self, *args, **kwargs):
        # If student is approved and has no student_id, generate one
        if self.status == "Regular" and not self.student_id:
            current_year = datetime.datetime.now().year % 100  # Get last two digits of the year
            unique_number = Student.objects.filter(student_id__startswith=f"TESP-{current_year}").count() + 1
            self.student_id = f"TESP-{current_year}-{str(unique_number).zfill(4)}"
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        archived_account = ArchivedAccount(student=self)
        archived_account.save()
        super().delete(*args, **kwargs)
        
        
        
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_type = models.CharField(max_length=20, choices=[('new', 'New Student'), ('transfer', 'Transferee')])
    previous_school = models.CharField(max_length=255, blank=True, null=True)
    transfer_reason = models.TextField(blank=True, null=True)
    grade_level = models.CharField(max_length=20)
    kindergarten_certificate = models.FileField(upload_to='documents/', blank=True, null=True)
    transferee_report_card = models.FileField(upload_to='documents/', blank=True, null=True)
 
 
class EnrollmentPeriod(models.Model):   
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return f"{self.start_date} - {self.end_date}" 
 
        
class Mother(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()

    # Mother's address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='mother')

class Father(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20)
    occupation = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()

    # Father's address fields
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='father')

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    file_uploaded = models.FileField(upload_to='documents/')

class ArchivedAccount(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    archived_on = models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='schedules', blank=True, null=True)
    grade_level = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=50)
    mon_7 = models.CharField(max_length=100, blank=True, null=True)
    tue_7 = models.CharField(max_length=100, blank=True, null=True)
    wed_7 = models.CharField(max_length=100, blank=True, null=True)
    thu_7 = models.CharField(max_length=100, blank=True, null=True)
    fri_7 = models.CharField(max_length=100, blank=True, null=True)
    schedule_section = models.OneToOneField('Section', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"Schedule for Grade {self.grade_level}"


class Section(models.Model): 
    grade_level = models.CharField(max_length=20)
    section = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.grade_level} - {self.section}" 
    
class Subject(models.Model):
    name = models.CharField(max_length=50)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        return self.name 
    