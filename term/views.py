from term.models import *
from term.serializers import *
from term.filters import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import *

class TermAPIView(ModelViewSet):
    filter_backends = (SubjectFilter,)

class SubjectView(TermAPIView):
    model = SubjectField
    serializer_class = SubjectSerializer
    lookup_field = 'name'

class ConceptView(TermAPIView):
    model = Concept
    serializer_class = ConceptSerializer
    lookup_field = 'name'

