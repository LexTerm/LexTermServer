from rest_framework.viewsets import ModelViewSet
from term.models import SubjectField, Concept, Note


class SubjectFieldView(ModelViewSet):
    model = SubjectField
    #serializer_class = SubjectSerializer


class ConceptView(ModelViewSet):
    model = Concept
    #serializer_class = ConceptSerializer


class NoteView(ModelViewSet):
    model = Note
