from rest_framework import serializers

from project.base.apps.tags.models import DocumentTags, HighlightedText


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTags
        fields = ['id', 'name', 'pdf_documents', 'parent_tag', 'color']


class HighlightedTextSerializer(serializers.ModelSerializer):
    document_tags = TagsSerializer()

    class Meta:
        model = HighlightedText
        fields = ['selected_text', 'document_tags', 'pdf_documents', 'all_doc_tagged', 'id', 'start_of_selection']
