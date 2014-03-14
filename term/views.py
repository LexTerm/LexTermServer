from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from term.models import SubjectField, Concept, Note
from term.serializers import SubjectFieldSerializer, \
    ConceptSerializer, NoteSerializer, ConceptListSerializer, \
    SubjectFieldListSerializer
from term.filters import SubjectFieldFilter, ConceptFilter, \
    NoteFilter
from lex.serializers import LexemeSerializer


class SubjectFieldView(ModelViewSet):
    model = SubjectField
    serializer_class = SubjectFieldSerializer
    filter_class = SubjectFieldFilter

    #def list(self, request):
        #query = self.get_queryset()
        #query = SubjectFieldFilter(request.GET, query)
        #serializer = SubjectFieldListSerializer(query)
        #return Response(serializer.data)


class ConceptView(ModelViewSet):
    model = Concept
    serializer_class = ConceptSerializer
    filter_class = ConceptFilter

    #def list(self, request):
        #query = self.get_queryset()
        #query = ConceptFilter(request.GET, query)
        #serializer = ConceptListSerializer(query)
        #return Response(serializer.data)

    @link()
    def lexemes(self, request, pk=None):
        obj = self.get_object()
        serializer = LexemeSerializer(obj.lexemes.all())
        return Response(serializer.data)


    @link()
    def subject_fields(self, request, pk=None):
        obj = self.get_object()
        serializer = SubjectFieldSerializer(obj.subject_fields.all())
        return Response(serializer.data)


class NoteView(ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_class = NoteFilter
