# urls.py
from django.urls import path
from .views import (
    YearsListAPIView,
    FacultyListAPIView, FacultyDetailAPIView,
    CourseListAPIView, CourseDetailAPIView,
    DepartmentDetailAPIView, DepartmentListAPIView,
    QuestionPaperListAPIView, QuestionPaperDetailAPIView, StartQSession, SendMessage
)

urlpatterns = [
    path('qsession/', StartQSession.as_view(), name='start_qsession'),
    path('messages/', SendMessage.as_view(), name='send_message'),
    path('faculties/', FacultyListAPIView.as_view(), name='faculty-list'),
    path('faculties/<int:pk>/', FacultyDetailAPIView.as_view(), name='faculty-detail'),
    path('departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department-detail'),
    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('question-papers/', QuestionPaperListAPIView.as_view(), name='question-paper-list'),
    path('question-papers/<int:pk>/', QuestionPaperDetailAPIView.as_view(), name='question-paper-detail'),
    path('years/', YearsListAPIView.as_view(), name='years-list'),
]

