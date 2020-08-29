from rest_framework.views import APIView
from project.base.apps.tags.documents import PdfFileDocument
from rest_framework.response import Response


class SearchText(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if query:
            searched_result = PdfFileDocument.search().query('match', text=query).highlight('text', type="plain",
                                                                                            fragment_size=500,
                                                                                            number_of_fragments=5000).highlight_options(
                order='score', pre_tags=["<b class='red'>"], post_tags=["</b>"])
            resp = searched_result.execute()
            resp_dict = resp.to_dict()
            return Response(resp_dict['hits'])
