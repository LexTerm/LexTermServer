from lex.models import *
from lex.serializers import *
from lex.filters import *
# from django.http import Http404
# from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import *
# from rest_framework import status
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)

# Lex Root
@api_view(('GET',))
def lex_root(request, format=None):
    return Response({
        '_links': {
            'languages': reverse('language_list', request=request, format=format),
        }
    })

class LexAPIView(ModelViewSet):
    filter_backends = (LanguageFilter,)

class LanguageView(ModelViewSet):
    # queryset = Language.objects.all()
    model = Language
    serializer_class = LanguageSerializer
    lookup_field = 'langCode'

class LexemeView(LexAPIView):
    model = Lexeme
    serializer_class = LexemeSerializer
    lookup_field = 'id'

class LexicalFormView(LexAPIView):
    model = LexicalForm
    filter_backends = (LexemeFilter,)
    serializer_class = LexicalFormSerializer
    lookup_field = 'form'

class LexicalClassView(LexAPIView):
    model = LexicalClass
    serializer_class = LexicalClassSerializer
    lookup_field = 'name'

class RepTypeView(LexAPIView):
    model = RepresentationType
    serializer_class = RepTypeSerializer
    lookup_field = 'name'

class EnumView(LexAPIView):
    model = Enumeration
    lookup_field = 'name'
    serializer_class = EnumSerializer


# class EnumValueView(ModelViewSet):
class EnumValueView(LexAPIView):
    model = EnumValue
    filter_backends = (EnumFilter,)
    serializer_class = EnumValueSerializer
    lookup_field = 'value'



# class LexFilteredAPIView(ModelViewSet):
#     def get_queryset(self):
#         queryset = self.model._default_manager.all()
#         filter = {}
#         for field in self.list_lookup_fields:
#             filter[field] = self.kwargs[field]
#         return queryset.filter(**filter)
#         # return get_list_or_404(queryset, **filter)
# 
#     def get_object(self):
#         queryset = self.get_queryset()
#         lookup = self.kwargs.get(self.lookup_field)
#         filter = {self.lookup_field: lookup}
#         return get_object_or_404(queryset, **filter)
