from django.urls import path
from .views import ConvertDocToPDFView, ConvertPDFToDocView

urlpatterns = [
    path('convert/doc-to-pdf/', ConvertDocToPDFView.as_view(), name='convert-doc-to-pdf'),
    path('convert/pdf-to-doc/', ConvertPDFToDocView.as_view(), name='convert-pdf-to-doc'),
]
