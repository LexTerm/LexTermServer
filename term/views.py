from term.models import *
from term.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import *

class SubjectView(ListCreateAPIView):
    model = SubjectField
    serializer_class = SubjectSerializer
    lookup_field = 'name'

class ConceptList(APIView):
    def get(self, request, subject=None, format=None):
        return Response(None)

class Concept(APIView):
    def get(self, request, id, subject=None, format=None):
        return Response(None)
		
class Lemma(APIView):
    def get(self, request, lemma, subject=None, format=None):
        return Response(None)
