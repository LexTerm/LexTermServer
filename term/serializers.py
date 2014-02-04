from rest_framework.serializers import ModelSerializer  # , RelatedField
from term.models import Concept, Note, SubjectField


class SubjectFieldSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('id', 'name')


class ConceptSerializer(ModelSerializer):
    #subjectFields = RelatedField(many=True)
    class Meta:
        model = Concept
        fields = ('id', 'concept_id', 'definition')


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note_type', 'note', 'lexeme')
