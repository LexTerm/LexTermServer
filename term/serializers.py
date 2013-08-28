from django.forms import widgets
from rest_framework import serializers
from term.models import *

# Serializers for termbase API

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('name',)

# class LexemeSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         model = LexemeTerm
#         fields = ('name', 'language', 'concept', 'termNote', 'usage')
# 
