from rest_framework import serializers
from .models import Faculty, Department, Course, QuestionPaper, QSession, Message


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Department
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class QuestionPaperSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = QuestionPaper
        fields = "__all__"


class QSessionSerializer(serializers.ModelSerializer):
    question_paper = QuestionPaperSerializer(read_only=True)
    class Meta:
        model = QSession
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
