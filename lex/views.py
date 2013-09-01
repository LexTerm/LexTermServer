from lex.models import *
from lex.serializers import *
from lex.filters import LanguageFilter, EnumFilter
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import *
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

class LexAPIView(ModelViewSet):
    filter_backends = (LanguageFilter,)

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

class LanguageView(ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class LexicalClassView(LexAPIView):
    model = LexicalClass
    serializer_class = LexicalClassSerializer
    lookup_field = 'name'

class RepTypeView(LexAPIView):
    model = RepresentationType
    serializer_class = RepTypeSerializer
    lookup_field = 'name'

# class EnumView(LexAPIView):
class EnumView(LexAPIView):
    model = Enumeration
    serializer_class = EnumSerializer
    lookup_field = 'name'

# class EnumValueView(ModelViewSet):
class EnumValueView(LexAPIView):
    model = EnumValue
    filter_backends = (EnumFilter,)
    serializer_class = EnumValueSerializer
    lookup_field = 'value'

class LexemeView(LexAPIView):
    model = LexemeTerm
    serializer_class = LexemeSerializer
    lookup_field = 'id'

