from rest_framework import serializers

from project.base.apps.tags.models import HighlightedText


class HighlightedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightedText
        fields = ['selected_text', 'document_tags', 'pdf_documents', 'all_doc_tagged', 'id', 'start_of_selection']

    def create(self, validated_data):
        instance = super().create(validated_data)
        tag_instance = validated_data['document_tags']
        pdf_instance = validated_data['pdf_documents']
        tag_instance.pdf_documents.add(pdf_instance)
        return instance
