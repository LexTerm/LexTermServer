from term.models import *
from term.serializers import *
from term.filters import *
from tbx.views import tbx_root
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Term Root
@api_view(('GET',))
def term_root(request, format=None):
    return Response({
        '_links': {
            'concepts': reverse('concept_view', request=request, format=format),
            'subjects': reverse('subject_view', request=request, format=format),
            'tbx': reverse(tbx_root, request=request, format=format),
        }
    })

class TermAPIView(ModelViewSet):
    filter_backends = (SubjectFilter,)

class SubjectView(TermAPIView):
    model = SubjectField
    serializer_class = SubjectSerializer
    lookup_field = 'name'

class ConceptView(TermAPIView):
    model = Concept
    serializer_class = ConceptSerializer
    lookup_field = 'id'

