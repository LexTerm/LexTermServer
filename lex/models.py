from django.db import models
from config.models import *
from term.models import *

class Lexeme(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)
    term = models.ForeignKey(Term, related_name='relatedLexeme')

    def __unicode__(self):
        return self.name

class Representation(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    representationType = models.ForeignKey(RepresentationType)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class PartOfSpeech(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    lexicalClass = models.ForeignKey(LexicalClass)

    def __unicode__(self):
        return self.lexicalClass

class FeatureSet(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s" % (self.lexeme, self.value)

class WordSense(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    concept = models.ForeignKey(Concept)
    etymology = models.TextField()
    
    def __unicode__(self):
        return "%s:%s" % (self.lexeme, self.concept)

