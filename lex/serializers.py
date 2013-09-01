from django.forms import widgets
from rest_framework import serializers
from lex.models import *

# Serializers for Lexicon API

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name', 'langCode')

class LexicalClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LexicalClass
        fields = ('name', 'language')

class EnumValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumValue
        fields = ('value', 'enum')

class EnumSerializer(serializers.ModelSerializer):
    # def get_related_field(self, model_field, related_model, to_many):
    #     kwargs = {
    #         'queryset': related_model.objects.filter(enum=model_field.name),
    #         'many': to_many
    #     }
    # name = serializers.CharField()
    # qset = EnumValue.objects.filter(enum=name)
    # values = serializers.SlugRelatedField(many=True, slug_field='value')
    values = serializers.RelatedField(many=True)
    # values = EnumValueSerializer(many=True)

    class Meta:
        model = Enumeration
        fields = ('name', 'language', 'values')

class RepTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('name', 'language')

class LexemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LexemeTerm
        fields = ('id', 'name', 'language', 'concept')

class FormSerializer(serializers.ModelSerializer):
    values = serializers.RelatedField(many=True)

    class Meta:
        model = Form
        fields = ('name', 'principle', 'lexicalClass', 'derivedLexicalClass', 'values')

# class LexicalClassSerializer(serializers.ModelSerializer):
#     class Meta:

