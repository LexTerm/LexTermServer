from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from lex.views import lex_root
from term.views import term_root

# API Root
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        '_links': {
            'lex': reverse(lex_root, request=request, format=format),
            'term': reverse(term_root, request=request, format=format)
        }
    })

