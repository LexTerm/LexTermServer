from django.forms import widgets
from rest_framework.serializers import ModelSerializer
from term.models import *

# Serializers for termbase API

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('name',)

class ConceptSerializer(ModelSerializer):
    class Meta:
        model = Concept
        fields = ('name', 'subjectField')

# class LexemeSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         model = LexemeTerm
#         fields = ('name', 'language', 'concept', 'termNote', 'usage')
# 
