from django.shortcuts import render
# from rest_framework import viewsets, filters, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Faculty, Professor, Student, Course, Semester, ClassSchedule, Enrollment
# from .serializers import (FacultySerializer, ProfessorSerializer, StudentSerializer,
#                          CourseSerializer, SemesterSerializer, ClassScheduleSerializer,
#                          EnrollmentSerializer)
#
# class FacultyViewSet(viewsets.ModelViewSet):
#     queryset = Faculty.objects.all()
#     serializer_class = FacultySerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'code']
#     ordering_fields = ['name', 'code']
#
# class ProfessorViewSet(viewsets.ModelViewSet):
#     queryset = Professor.objects.all()
#     serializer_class = ProfessorSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['faculty', 'academic_rank']
#     search_fields = ['first_name', 'last_name', 'personnel_code']
#     ordering_fields = ['last_name', 'hire_date']
#
#     @action(detail=True, methods=['get'])
#     def classes(self, request, pk=None):
#         professor = self.get_object()
#         classes = ClassSchedule.objects.filter(professor=professor)
#         serializer = ClassScheduleSerializer(classes, many=True)
#         return Response(serializer.data)
#
# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['faculty', 'degree', 'is_active', 'entry_year']
#     search_fields = ['first_name', 'last_name', 'student_number']
#     ordering_fields = ['last_name', 'entry_year']
#
#     @action(detail=True, methods=['get'])
#     def enrollments(self, request, pk=None):
#         student = self.get_object()
#         enrollments = Enrollment.objects.filter(student=student)
#         serializer = EnrollmentSerializer(enrollments, many=True)
#         return Response(serializer.data)
#
# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['faculty', 'units']
#     search_fields = ['name', 'code']
#     ordering_fields = ['name', 'code']
#
#     @action(detail=True, methods=['get'])
#     def classes(self, request, pk=None):
#         course = self.get_object()
#         classes = ClassSchedule.objects.filter(course=course)
#         serializer = ClassScheduleSerializer(classes, many=True)
#         return Response(serializer.data)
#
# class SemesterViewSet(viewsets.ModelViewSet):
#     queryset = Semester.objects.all()
#     serializer_class = SemesterSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['year', 'semester', 'is_active']
#     ordering_fields = ['year', 'semester']
#
#     @action(detail=True, methods=['post'])
#     def set_active(self, request, pk=None):
#         semester = self.get_object()
#         Semester.objects.all().update(is_active=False)
#         semester.is_active = True
#         semester.save()
#         return Response({'status': 'semester activated'})
#
# class ClassScheduleViewSet(viewsets.ModelViewSet):
#     queryset = ClassSchedule.objects.all()
#     serializer_class = ClassScheduleSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['course', 'professor', 'semester', 'day']
#     search_fields = ['course__name', 'professor__last_name']
#     ordering_fields = ['course__name', 'start_time']
#
#     @action(detail=True, methods=['get'])
#     def enrollments(self, request, pk=None):
#         class_schedule = self.get_object()
#         enrollments = Enrollment.objects.filter(class_schedule=class_schedule)
#         serializer = EnrollmentSerializer(enrollments, many=True)
#         return Response(serializer.data)
#
# class EnrollmentViewSet(viewsets.ModelViewSet):
#     queryset = Enrollment.objects.all()
#     serializer_class = EnrollmentSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['student', 'class_schedule', 'grade']
#     ordering_fields = ['enrollment_date', 'grade']
#
#     def create(self, request, *args, **kwargs):
#         try:
#             return super().create(request, *args, **kwargs)
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# Home View
def homePage(request):
    return render(request, 'general/index.html', context={})
def contactUS(request):
    return render(request, 'general/contactUs.html', context={})

# Login View
def login(request):
    return render(request, "general/login.html", context={})