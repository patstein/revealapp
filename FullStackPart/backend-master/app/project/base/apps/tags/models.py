from django.db import models


class DocumentTags(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=200,
    )

    pdf_documents = models.ManyToManyField(
        verbose_name='pdf_documents',
        related_name='document_tags',
        to='tags.PdfDocuments',
        blank=True
    )

    parent_tag = models.ForeignKey(
        verbose_name='parent_tag',
        related_name='children',
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    color = models.CharField(
        verbose_name='color',
        max_length=7
    )

    def __str__(self):
        return str(self.name)


class PdfDocuments(models.Model):
    pdf = models.FileField(upload_to='./pdfs', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name="text", null=True)
    html_text = models.TextField(verbose_name="html_text", null=True)
    html_created = models.BooleanField(verbose_name='html_created', default=False)
    text_created = models.BooleanField(verbose_name='html_created', default=False)
    html_text_created = models.BooleanField(verbose_name='html_text_created', default=False)

    def __str__(self):
        return str(self.pdf)


class HighlightedText(models.Model):
    selected_text = models.TextField(
        verbose_name='selected_text',
        blank=True,
    )
    document_tags = models.ForeignKey(
        verbose_name='document_tags',
        related_name='highlighted_text',
        to='tags.DocumentTags',
        on_delete=models.CASCADE,

    )
    pdf_documents = models.ForeignKey(
        verbose_name='pdf_documents',
        related_name='highlighted_text',
        to='tags.PdfDocuments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    all_doc_tagged = models.BooleanField(
        verbose_name='all_doc_tagged',
        default=False
    )

    start_of_selection = models.IntegerField(
        verbose_name='start_of_selection',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.selected_text)
