from django.urls import path

from project.apps.tags.views import GetTags, GetHighlightedTextOfTag, GetHighlightedTextOfPdf

urlpatterns = [
    path('', GetTags.as_view(), name='get-tags'),
    path('phrases/<int:pk>/', GetHighlightedTextOfTag.as_view(), name='get-phrases'),
    path('pdfs/phrases/<int:pk>/', GetHighlightedTextOfPdf.as_view(), name='get-phrases')

]
