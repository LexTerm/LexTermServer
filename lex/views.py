from lex.models import *
from lex.serializers import *
from lex.filters import LanguageFilter, NameFilter, IDFilter
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import *
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

# Doesn't work yet. lookup_field doesn't seem to work. Why?
# maybe because I wasn't adding a handler for the RetrieveModelMixin
class LexAPIView(ModelViewSet):
    filter_backends = (LanguageFilter,)

    # def get_queryset(self):
    #     logger.error('self.action: {}'.format(self.action))
    #     return self.filter_queryset(super(LexAPIView, self).get_queryset())

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def get_object(self, queryset):
    #     logger.error('self.lookup_field: {}'.format(self.lookup_field))
    #     queryset = self.get_queryset()
    #     lookup = self.kwargs.get(self.lookup_field)
    #     filter_kwargs = {self.lookup_field: lookup}
    #     return get_object_or_404(queryset, **filter_kwargs)

# class LexAPIView(RetrieveModelMixin,
#                  DestroyModelMixin,
#                  ListCreateAPIView):
#     """
#     Generic API View with retrieve, list, and create mixins
#     """
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

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

class EnumView(LexAPIView):
    model = Enumeration
    serializer_class = EnumSerializer
    lookup_field = 'name'

# class EnumValueView(LexAPIView):
#     serializer_class = EnumValueSerializer
#     queryset = Enumeration.objects.all()
#     filter_backends = ()

class LexemeView(LexAPIView):
    model = LexemeTerm
    serializer_class = LexemeSerializer
    lookup_field = 'id'

