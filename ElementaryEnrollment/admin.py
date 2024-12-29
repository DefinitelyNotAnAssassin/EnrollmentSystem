from django.contrib import admin
from ElementaryEnrollment.models import Student, Enrollment, Mother, Father, Document, ArchivedAccount, Schedule, Section, Subject, EnrollmentPeriod

# Register your models here. 

admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Mother)
admin.site.register(Father)
admin.site.register(Document)
admin.site.register(ArchivedAccount)
admin.site.register(Schedule)
admin.site.register(Subject)
admin.site.register(EnrollmentPeriod)
class StudentInline(admin.TabularInline):
    model = Student
    extra = 1  
@admin.register(Section)  
class SectionAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    
class RegistrarAdminMixin:
    def has_module_permission(self, request):
        if request.user.groups.filter(name='Registrar').exists():
            return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.groups.filter(name='Registrar').exists():
            return True
        return super().has_view_permission(request, obj)
