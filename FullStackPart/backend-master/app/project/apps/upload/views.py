from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from project.base.apps.tags.models import PdfDocuments
from project.apps.upload.serializer import FileSerializer


class FileView(APIView):
    """
    View to upload file, convert it to html and text.
    """
    permission_classes = []

    def post(self, request, **kwargs):
        myfile = request.FILES['filepond']
        instance = PdfDocuments(pdf=myfile)
        instance.save()
        return HttpResponse("Working upload")


class GetPdfs(ListAPIView):
    """
    View to get pdf related information based on the id of the pdfs passed in the GET request.
    """
    permission_classes = []
    serializer_class = FileSerializer

    def get_queryset(self):
        params = self.request.query_params
        indexes = []
        for param in params:
            indexes.append(params[param])
        return PdfDocuments.objects.filter(id__in=indexes)


class GetAllPdfs(ListAPIView):
    """
    View to get all pdf info.
    """
    permission_classes = []
    serializer_class = FileSerializer

    def get_queryset(self):
        return PdfDocuments.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for pdf in list(queryset):
            pdf.text = self.tagPdf(pdf)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @staticmethod
    # def tagPdf(pdf):
    #     text = pdf.text
    #     highlighted_texts = pdf.highlighted_text
    #     for highlight in list(highlighted_texts.all()):
    #         index1 = text.find(highlight.selected_text)
    #         if index1 == -1:
    #             continue
    #         index2 = index1 + len(highlight.selected_text)
    #
    #         beginning = text[:index1]
    #         match = text[index1:index2]
    #         end = text[index2:]
    #
    #         text = \
    #             beginning + '<span class="tagclass" title="' + \
    #             highlight.document_tags.name + \
    #             '" style="background-color:' + \
    #             highlight.document_tags.color + '">' + \
    #             match + '</span>' + end
    #
    #     return text

    @staticmethod
    def tagPdf(pdf):
        text = pdf.text
        highlighted_texts = pdf.highlighted_text
        for highlight in list(highlighted_texts.all().order_by('-start_of_selection')):
            index1 = highlight.start_of_selection
            if index1 == -2:
                index1 = text.find(highlight.selected_text)
            if index1 == -1 or index1 is None:
                continue
            index2 = index1 + len(highlight.selected_text)

            beginning = text[:index1]
            match = text[index1:index2]
            end = text[index2:]

            text = \
                beginning + '<span class="tagclass" title="' + \
                highlight.document_tags.name + \
                '" style="background-color:' + \
                highlight.document_tags.color + '">' + \
                match + '</span>' + end

        return text

    @staticmethod
    def tagHTML(pdf):
        text = pdf.html_text
        # highlighted_texts = pdf.highlighted_text
        # for highlight in list(highlighted_texts.all()):
        #     index1 = text.find(highlight.selected_text)
        #     if index1 == -1:
        #         continue
        #     index2 = index1 + len(highlight.selected_text)
        #
        #     beginning = text[:index1]
        #     match = text[index1:index2]
        #     end = text[index2:]
        #
        #     text = beginning + '<span class="tagclass" title="' +
        # highlight.document_tags.name + '" style="background-color:' +
        # highlight.document_tags.color + '">' + match + '</span>' + end

        return text
