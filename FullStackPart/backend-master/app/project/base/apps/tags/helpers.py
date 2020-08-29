import os
import pdftotext
from bs4 import BeautifulSoup
from django.conf import settings


def converting_pdf_to_text(instance):
    myfile = instance.pdf
    with open(f'{settings.MEDIA_ROOT}/{myfile}', "rb") as f:
        pdf = pdftotext.PDF(f)
        complete_pdf = ("\n\n".join(pdf))
        # uncommented for formatting
        # complete_pdf_no_ext_spaces = ' '.join(complete_pdf.split())
        instance.text = complete_pdf
        instance.text_created = True
        instance.save()


def converting_pdf_to_html(myfile):
    os.system(f'pdf2htmlEX --zoom 1.3 {settings.MEDIA_ROOT}/{myfile} --dest-dir {settings.MEDIA_ROOT}/htmls/')


def convert_html_to_html_text(myfile):
    style_html_text = ''

    with open(f'{settings.MEDIA_ROOT}/htmls/{str(myfile)[5:-4]}.html', "rb") as file:
        data = file.read()
        soup = BeautifulSoup(data, 'html.parser')
        for style in soup.find_all('style'):
            # if str(style) containes #page-container -> remove
            style_html_text += str(style)
        style_html_text += '<style>#page-container {background-color: #cccccc; position: relative; ' \
                           'background-image: url('') !important;}</style>'
        div1 = soup.find("div", {"id": "page-container"})
        full_text = style_html_text + str(div1)
    return full_text
