from rest_framework.viewsets import ModelViewSet
from term.models import SubjectField, Concept, Note
from term.serializers import SubjectFieldSerializer, \
    ConceptSerializer, NoteSerializer
from term.filters import SubjectFieldFilter, ConceptFilter, \
    NoteFilter


class SubjectFieldView(ModelViewSet):
    model = SubjectField
    serializer_class = SubjectFieldSerializer
    filter_class = SubjectFieldFilter


class ConceptView(ModelViewSet):
    model = Concept
    serializer_class = ConceptSerializer
    filter_class = ConceptFilter


class NoteView(ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_class = NoteFilter
