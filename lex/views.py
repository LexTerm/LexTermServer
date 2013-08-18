from lex.models import *
from lex.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

class LanguageList(generics.ListAPIView):
    model = Language
    serializer_class = LanguageSerializer

# class LangList(APIView):
#     def get(self, request, format=None):
#         langs = Language.objects.all()
#         serializer = LanguageSerializer(langs, many=True)
#         return Response(serializer.data)

class LexicalClassList(APIView):
    def get(self, request, lang, format=None):
        classes = LexicalClass.objects.filter(language=lang)
        serializer = LexicalClassSerializer(classes, many=True)
        return Response(serializer.data)
    
    # def post(self, request, lang, format=None):
    #     return Response(None)
	
class RepTypeList(APIView):
    def get(self, request, lang, format=None):
        reps = RepresentationType.objects.filter(language=lang)
        serializer = RepTypeSerializer(reps, many=True)
        return Response(serializer.data)

# class RepList(APIView):
#     def get(self, request, lang, format=None):
#         return Response(None)
	
class EnumView(APIView):
    def get(self, request, lang, enum_name=None, format=None):
        if enum_name == None:
            enums = Enumeration.objects.filter(language=lang)
            serializer = EnumSerializer(enums, many=True)
        else:
            enum = Enumeration.objects.filter(language=lang, name=enum_name)
            serializer = EnumSerializer(enum, many=True)
        return Response(serializer.data)

# class EnumList(APIView):
#     def get(self, request, lang, format=None):
#         return Response(None)

class Enum(APIView):
    def get(self, request, lang, enum_name, format=None):
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
    
