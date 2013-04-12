from lex.models import *
from lex.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LangList(APIView):
    def get(self, request, format=None):
        return Response(None)

class EnumList(APIView):
    def get(self, request, lang, format=None):
        return Response(None)

class Enum(APIView):
    def get(self, request, lang, enum_name, format=None):
        return Response(None)
		
class RepList(APIView):
    def get(self, request, lang, format=None):
        return Response(None)
	
class LexClassList(APIView):
    def get(self, request, lang, format=None):
        return Response(None)
    
    def post(self, request, lang, format=None):
        return Response(None)
	
class LexClass(APIView):
    def get(self, request, lang, class_name, format=None):
        return Response(None)
		
    def put(self, request, lang, class_name, format=None):
        return Response(None)
	
class LexemeList(APIView):
    def get(self, request, lang, lemma=None, format=None):
        return Response(None)
    
    def post(self, request, lang, lemma=None, format=None):
        return Response(None)
		
class Lexeme(APIView):
    def get(self, request, lang, id, format=None):
        return Response(None)
	
    def put(self, request, lang, id, format=None):
        return Response(None)
    