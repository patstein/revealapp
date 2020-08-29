from rest_framework import serializers

from project.base.apps.tags.models import PdfDocuments


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = PdfDocuments
        fields = ('pdf', 'timestamp', 'text', 'id')
