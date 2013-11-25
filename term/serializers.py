from django.forms import widgets
from rest_framework.serializers import ModelSerializer, RelatedField
from term.models import *

# Serializers for termbase API

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('name',)

class ConceptSerializer(ModelSerializer):
    subjectFields = RelatedField(many=True)
    class Meta:
        model = Concept
        fields = ('id', 'subjectFields', 'definition')

# class LexemeSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         model = LexemeTerm
#         fields = ('name', 'language', 'concept', 'termNote', 'usage')
# 
