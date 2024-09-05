from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import PyPDF2
from io import BytesIO

User = get_user_model()


class Faculty(models.Model):
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="departments"
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=False)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="courses"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="courses"
    )

    def __str__(self):
        return self.name


class QuestionPaper(models.Model):
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='question_papers', null=True, blank=True)
   
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="question_papers"
    )
   
    document = models.FileField(upload_to="question_papers/")
    content = models.TextField(blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.course.name} - {self.year} {self.semester}"

    def clean(self):
        super().clean()
        if self.document:
            self.validate_pdf(self.document)

    def validate_pdf(self, pdf_file):
        if not pdf_file.name.endswith(".pdf"):
            raise ValidationError("The file must be a PDF.")
        try:
            pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_file.read()))
            if pdf_reader.isEncrypted:
                raise ValidationError("The PDF file is encrypted.")
        except PyPDF2.utils.PdfReadError:
            raise ValidationError("The file is not a valid PDF.")
        finally:
            pdf_file.seek(0)  # Reset file pointer after reading

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call clean() and validate the file
        if self.document:
            self.content = self.extract_text_from_pdf(self.document)
        super().save(*args, **kwargs)

    def extract_text_from_pdf(self, pdf_file):
        pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_file.read()))
        text = ""
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            text += page.extract_text()
        pdf_file.seek(0)  # Reset file pointer after reading
        return text


class QSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qsessions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.question_paper.course.name}"


class Message(models.Model):
    qsession = models.ForeignKey(
        QSession, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    ai_response = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
