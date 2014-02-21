from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from term.models import SubjectField, Concept, Note
from term.serializers import SubjectFieldSerializer, \
    ConceptSerializer, NoteSerializer
from term.filters import SubjectFieldFilter, ConceptFilter, \
    NoteFilter
from lex.serializers import LexemeSerializer


class SubjectFieldView(ModelViewSet):
    model = SubjectField
    serializer_class = SubjectFieldSerializer
    filter_class = SubjectFieldFilter


class ConceptView(ModelViewSet):
    model = Concept
    serializer_class = ConceptSerializer
    filter_class = ConceptFilter

    @link()
    def lexemes(self, request, pk=None):
        obj = self.get_object()
        serializer = LexemeSerializer(obj.lexemes.all())
        return Response(serializer.data)


class NoteView(ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_class = NoteFilter
