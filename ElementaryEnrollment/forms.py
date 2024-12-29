# forms.py
from django import forms
from .models import Student, Mother, Father, Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Enrollment  # Enrollment model to capture additional enrollment information


class StudentForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Student
        fields = [
            'student_id','last_name', 'first_name', 'middle_name', 'suffix', 'birth_date', 'sex', 'email',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for student
        ]
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name','middle_name', 'last_name', 'birth_date', 'sex', 'email', 'street', 'barangay', 'city', 'state_province', 'country']

class MotherForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mother
        fields = [
            'last_name', 'first_name', 'middle_name', 'contact', 'occupation', 'birth_date',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for mother
        ]

class FatherForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Father
        fields = [
            'last_name', 'first_name', 'middle_name', 'contact', 'occupation', 'birth_date',
            'street', 'barangay', 'city', 'state_province', 'country'  # New address fields for father
        ]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file_uploaded']

class CreateAccountForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        help_text="Username should be in format TESP-XX-XXXX",
        widget=forms.TextInput(attrs={'placeholder': 'TESP-XX-XXXX'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^TESP-\d{2}-\d{4}$', username):
            raise forms.ValidationError("Username must follow the format TESP-XX-XXXX.")
        return username

class EnrollmentFormNewStudent(forms.ModelForm):
    kindergarten_certificate = forms.FileField(required=True)

    class Meta:
        model = Enrollment
        fields = ['student_type', 'kindergarten_certificate', 'student']  

class EnrollmentFormTransferee(forms.ModelForm):
    transferee_report_card = forms.FileField(required=True)

    class Meta:
        model = Enrollment
        fields = ['student_type', 'previous_school', 'transfer_reason', 'transferee_report_card']  # Adjust as needed

#Admin----------------------
class CreateRegistrarForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user