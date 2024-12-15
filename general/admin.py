from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Faculty, Professor, Student, Course, Semester, ClassSchedule, Enrollment

# تغییر عنوان‌های پنل ادمین
admin.site.site_header = 'مدیریت سیستم دانشگاه'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'مدیریت سیستم'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'code')
        }),
    )

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'faculty', 'personnel_code', 'academic_rank', 'hire_date', 'password')
    search_fields = ('first_name', 'last_name', 'personnel_code')
    list_filter = ('faculty', 'academic_rank')
    ordering = ('last_name', 'first_name')
    list_per_page = 20

    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': (('first_name', 'last_name'), 'national_code', 'password', 'birth_date', 
                      'gender', 'marital_status')
        }),
        ('اطلاعات دانشگاهی', {
            'fields': ('faculty', 'personnel_code', 'academic_rank', 'hire_date')
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_code', 'password', 'student_number')
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': (('first_name', 'last_name'), 'national_code', 'password', 'birth_date', 
                      'gender', 'marital_status')
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('faculty', 'student_number', 'entry_year', 'degree', 'is_active')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'units', 'faculty')
    search_fields = ('name', 'code')
    list_filter = ('faculty', 'units')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        ('اطلاعات درس', {
            'fields': ('name', 'code', 'units', 'faculty')
        }),
        ('پیش‌نیازها', {
            'fields': ('prerequisites',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('get_semester_display_admin', 'is_active')
    list_filter = ('year', 'semester', 'is_active')
    ordering = ('-year', '-semester')
    list_per_page = 20

    def get_semester_display_admin(self, obj):
        return f"{obj.get_semester_display()} {obj.year}"
    get_semester_display_admin.short_description = 'ترم تحصیلی'

    fieldsets = (
        ('اطلاعات ترم', {
            'fields': ('year', 'semester', 'is_active')
        }),
    )

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'professor', 'semester', 'get_day_display', 
                   'start_time', 'end_time', 'capacity')
    list_filter = ('course', 'professor', 'semester', 'day')
    search_fields = ('course__name', 'professor__last_name')
    ordering = ('semester', 'course')
    list_per_page = 20

    fieldsets = (
        ('اطلاعات کلاس', {
            'fields': ('course', 'professor', 'semester', 'capacity')
        }),
        ('زمان‌بندی', {
            'fields': ('day', ('start_time', 'end_time'))
        }),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_schedule', 'grade', 'enrollment_date')
    search_fields = ('student__first_name', 'student__last_name', 
                    'class_schedule__course__name')
    list_filter = ('class_schedule__course', 'enrollment_date', 'grade')
    ordering = ('-enrollment_date',)
    list_per_page = 20

    fieldsets = (
        ('اطلاعات ثبت‌نام', {
            'fields': ('student', 'class_schedule')
        }),
        ('نمره', {
            'fields': ('grade',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # در حالت ویرایش
            return ('enrollment_date',)
        return ()
