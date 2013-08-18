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

class EnumSerializer(serializers.ModelSerializer):
    values = serializers.RelatedField(many=True)

    class Meta:
        model = Enumeration
        fields = ('name', 'language', 'values')

class RepTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('name', 'language')

class FormSerializer(serializers.ModelSerializer):
    values = serializers.RelatedField(many=True)

    class Meta:
        model = Form
        fields = ('name', 'principle', 'lexicalClass', 'derivedLexicalClass', 'values')

# class LexicalClassSerializer(serializers.ModelSerializer):
#     class Meta:

