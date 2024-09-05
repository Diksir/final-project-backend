# views.py
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Faculty, Course, QuestionPaper, Message, QSession, Department
from .serializers import (
    FacultySerializer,
    CourseSerializer,
    QuestionPaperSerializer,
    MessageSerializer,
    QSessionSerializer,
    DepartmentSerializer,
)

from openai import OpenAI


class FacultyListAPIView(APIView):
    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(
            faculties, context={"request": request}, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class FacultyDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            faculty = Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FacultySerializer(faculty)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentListAPIView(APIView):
    def get(self, request):
        department = Department.objects.all().order_by("name")
        serializer = DepartmentSerializer(department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseListAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all().order_by("name")
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        papers = []
        for paper in QuestionPaper.objects.filter(course=course):
            papers.append(paper.year)

        serializer = CourseSerializer(course)
        response_data = {"course": serializer.data, "papers": papers}

        return Response(response_data, status=status.HTTP_200_OK)


class QuestionPaperListAPIView(APIView):
    def get(self, request):
        question_papers = QuestionPaper.objects.all()
        serializer = QuestionPaperSerializer(question_papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionPaperDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            question_paper = QuestionPaper.objects.get(pk=pk)
        except QuestionPaper.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionPaperSerializer(question_paper)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartQSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")

        user = request.user
        course = get_object_or_404(Course, id=course_id)

        question_paper = QuestionPaper.objects.filter(
            course=course,
        ).first()

        if not question_paper:
            return Response(status=status.HTTP_404_NOT_FOUND)

        qsession = QSession.objects.create(
            user=user, course=course, question_paper=question_paper
        )

        return Response(
            QSessionSerializer(qsession, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class SendMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qsession_id = request.data.get("qsession_id")
        content = request.data.get("content")
        user = request.user

        qsession = get_object_or_404(QSession, id=qsession_id)
        question_paper_content = qsession.question_paper.content

        message = Message.objects.create(
            qsession=qsession, sender=user, content=content
        )

        client = OpenAI(api_key=settings.OPEN_AI_API_KEY)

        prompt = f"Question Paper:\n{question_paper_content}\n\nUser: {content}"

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a student assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        ai_response = completion.choices[0].message.strip()

        message.ai_response = ai_response
        message.save()

        return Response(
            {
                "message": MessageSerializer(message).data,
            },
            status=status.HTTP_201_CREATED,
        )


class YearsListAPIView(APIView):
    def get(self, request):
        year_list = {}
        for year in QuestionPaper.objects.all():
            year_list[year.year] = year.year

        response_data = list(year_list.values())
        return Response(response_data)
