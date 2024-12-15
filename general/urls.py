from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter
# from .views import (FacultyViewSet, ProfessorViewSet, StudentViewSet,
#                    CourseViewSet, SemesterViewSet, ClassScheduleViewSet,
#                    EnrollmentViewSet)
#
# router = DefaultRouter()
# router.register(r'faculties', FacultyViewSet)
# router.register(r'professors', ProfessorViewSet)
# router.register(r'students', StudentViewSet)
# router.register(r'courses', CourseViewSet)
# router.register(r'semesters', SemesterViewSet)
# router.register(r'class-schedules', ClassScheduleViewSet)
# router.register(r'enrollments', EnrollmentViewSet)
app_name = "general"
urlpatterns = [
    # path('api/', include(router.urls)),
    path("", views.homePage, name="home"),
    path("contactUs", views.contactUS, name="contactUs"),
    path("login", views.login, name="login"),
    path("api/login/", views.LoginView.as_view(), name="api_login"),
    path("api/csrf/", views.get_csrf_token, name="csrf"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
