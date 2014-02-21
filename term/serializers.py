from rest_framework.serializers import ModelSerializer  # , RelatedField
from term.models import Concept, Note, SubjectField


class SubjectFieldSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('id', 'name', 'concepts')


class ConceptSerializer(ModelSerializer):
    class Meta:
        model = Concept
        fields = (
            'id', 'concept_id', 'definition', 'subject_fields', 'lexemes')


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note_type', 'note', 'lexeme')


class SubjectFieldListSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('id', 'name')


class ConceptListSerializer(ModelSerializer):
    class Meta:
        model = Concept
        fields = ('id', 'concept_id', 'definition')


class NoteListSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note_type', 'note', 'lexeme')
