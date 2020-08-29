from project.base.apps.tags.models import PdfDocuments
from rest_framework import serializers


class PdfDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfDocuments
        fields = '__all__'
