from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Professor
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
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


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        national_code = request.data.get('national_code')
        password = request.data.get('password')
        user_type = request.data.get('user_type', 'student')  # default to student

        if not national_code or not password:
            return Response({
                'error': 'لطفا کد ملی و رمز عبور را وارد کنید'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the user in either Student or Professor model
        try:
            if user_type == 'student':
                user = Student.objects.get(national_code=national_code)
            else:
                user = Professor.objects.get(national_code=national_code)

            if user.password == password:  # Note: This is not secure for real applications
                return Response({
                    'success': 'ورود موفقیت آمیز',
                    'user': {
                        'id': user.id,
                        'national_code': user.national_code,
                        'full_name': f"{user.first_name} {user.last_name}",
                        'user_type': user_type
                    }
                })
            else:
                return Response({
                    'error': 'رمز عبور اشتباه است'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except (Student.DoesNotExist, Professor.DoesNotExist):
            return Response({
                'error': 'کاربر یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)

# Add a dashboard view since we're redirecting to it
def dashboard(request):
    return render(request, 'general/dashboard.html')  # Create this template