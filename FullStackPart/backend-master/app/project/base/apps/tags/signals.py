from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PdfDocuments
from .helpers import converting_pdf_to_html, converting_pdf_to_text, convert_html_to_html_text


@receiver(post_save, sender=PdfDocuments)
def convert_pdf(sender, **kwargs):
    instance = kwargs.get('instance')
    if not instance.html_created:
        converting_pdf_to_html(instance.pdf)
        instance.html_created = True
        instance.save()
    if not instance.text_created:
        converting_pdf_to_text(instance)
        instance.save()
    if instance.html_created and not instance.html_text_created:
        text = convert_html_to_html_text(instance.pdf)
        instance.html_text = text
        instance.html_text_created = True
        instance.save()
