import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import convertapi
import os

CONVERTAPI_SECRET = 'ZVTWIn3nURW3T88s'
UPLOAD_LOCATION = "media/"

convertapi.api_secret = CONVERTAPI_SECRET

def generate_uuid_filename(extension):
    return f"{uuid.uuid4()}.{extension}"

def get_full_url(request, path):
    return request.build_absolute_uri(path)

class ConvertDocToPDFView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES["file"]
        extension = file.name.split('.')[-1]
        upload_filename = generate_uuid_filename(extension)
        fs = FileSystemStorage(location=UPLOAD_LOCATION)
        filename = fs.save(upload_filename, file)
        file_path = fs.path(filename)

        # Convert DOCX to PDF
        try:
            result = convertapi.convert('pdf', {'File': file_path})
            pdf_filename = generate_uuid_filename("pdf")
            pdf_path = os.path.join(UPLOAD_LOCATION, pdf_filename)
            result.file.save(pdf_path)

            pdf_url = get_full_url(request, fs.url(pdf_filename))
            return Response(
                {"status": "success", "file_url": pdf_url}
            )
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


class ConvertPDFToDocView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES["file"]
        extension = file.name.split('.')[-1]
        upload_filename = generate_uuid_filename(extension)
        fs = FileSystemStorage(location=UPLOAD_LOCATION)
        filename = fs.save(upload_filename, file)
        file_path = fs.path(filename)

        # Convert PDF to DOCX
        try:
            result = convertapi.convert('docx', {'File': file_path})
            doc_filename = generate_uuid_filename("docx")
            doc_path = os.path.join(UPLOAD_LOCATION, doc_filename)
            result.file.save(doc_path)

            doc_url = get_full_url(request, fs.url(doc_filename))
            return Response(
                {"status": "success", "file_url": doc_url}
            )
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)
