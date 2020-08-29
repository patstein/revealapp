from django.contrib import admin

from project.base.apps.tags.models import DocumentTags, PdfDocuments, HighlightedText

admin.site.register(DocumentTags)
admin.site.register(PdfDocuments)
admin.site.register(HighlightedText)
