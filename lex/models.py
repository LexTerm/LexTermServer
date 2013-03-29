from django.db import models
from config.models import *
from term.models import *

class Lexeme(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)
    term = models.ForeignKey(Term, related_name='relatedLexeme')

class Representation(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    representationType = models.ForeignKey(RepresentationType)
    name = models.CharField(max_length=100)

class PartOfSpeech(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    lexicalClass = models.ForeignKey(LexicalClass)

class FeatureSet(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    value = models.ForeignKey(EnumValue)

class WordSense(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    concept = models.ForeignKey(Concept)
    etymology = models.TextField()

