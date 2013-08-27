from lex.models import *
from lex.serializers import *
from lex.filters import LanguageFilter, NameFilter
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import status

class RetrieveListCreateAPIView(RetrieveModelMixin,
                                ListCreateAPIView):
    """
    Generic API View with retrieve, list, and create mixins
    """
    pass


class LanguageView(ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class LexicalClassView(RetrieveListCreateAPIView):
    serializer_class = LexicalClassSerializer
    queryset = LexicalClass.objects.all()
    filter_backends = (LanguageFilter, NameFilter,)

class RepTypeView(RetrieveListCreateAPIView):
    serializer_class = RepTypeSerializer
    queryset = RepresentationType.objects.all()
    filter_backends = (LanguageFilter, NameFilter,)

class EnumView(RetrieveListCreateAPIView):
    serializer_class = EnumSerializer
    queryset = Enumeration.objects.all()
    filter_backends = (LanguageFilter, NameFilter,)

# class LexemeView(RetrieveListCreateAPIView):
class LexemeView(ListAPIView):
    serializer_class = LexemeSerializer
    queryset = Lexeme.objects.all()
    filter_backends = (LanguageFilter, NameFilter,)

# class LexemeList(APIView):
#     def get(self, request, lang, lemma=None, format=None):
#         return Response(None)
#     
#     def post(self, request, lang, lemma=None, format=None):
#         return Response(None)
		
# class Lexeme(APIView):
#     def get(self, request, lang, id, format=None):
#         return Response(None)
# 	
#     def put(self, request, lang, id, format=None):
#         return Response(None)
    
