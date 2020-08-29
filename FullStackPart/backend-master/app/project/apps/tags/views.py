from rest_framework.generics import ListAPIView
from project.apps.tags.serializers import TagsSerializer, HighlightedTextSerializer
from project.base.apps.tags.models import DocumentTags, HighlightedText


class GetTags(ListAPIView):
    """
    View to get all tags and related info, such as the ID's of pdfs in which the tags have been used.
    """
    queryset = DocumentTags.objects.all()
    serializer_class = TagsSerializer


class GetHighlightedTextOfTag(ListAPIView):
    """
    View to get the texts (Key Phrases/Highlighted texts) that have been tagged with a specific tag (ID in url).
    """
    serializer_class = HighlightedTextSerializer

    def get_queryset(self):
        return HighlightedText.objects.filter(document_tags=self.kwargs['pk'])


class GetHighlightedTextOfPdf(ListAPIView):
    """
    View to get the texts (Key Phrases/Highlighted texts) for a specific pdf.
    """
    serializer_class = HighlightedTextSerializer

    def get_queryset(self):
        return HighlightedText.objects.filter(pdf_documents=self.kwargs['pk'])
