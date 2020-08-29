from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer, tokenizer
from .models import PdfDocuments

pdfDocument = Index('pdfdocuments')

pdfDocument.settings(
    number_of_shards=1,
    number_of_replicas=0
)

text_analyzer = analyzer(
    'text_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=4, max_gram=4),
    filter=["lowercase", "stop", "snowball"],
)


@pdfDocument.doc_type
class PdfFileDocument(DocType):
    text = fields.TextField(
        analyzer=text_analyzer,
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(multi=True),
            }
    )

    class Meta:
        model = PdfDocuments
        fields = ['pdf', 'html_created', 'text_created']
