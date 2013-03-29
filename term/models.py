from django.db import models
from config.models import *
from lex.models import *

class TermBase(models.Model):
    name = models.CharField(max_length=100)

class SubjectField(models.Model):
    name = models.CharField(max_length=100)

class Concept(models.Model):
    termBase = models.ForeignKey(TermBase)
    subjectField = models.ManyToManyField(SubjectField)
    superOrdinate = models.ForeignKey('self')

class ConceptDefinition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    definition = models.TextField()

class Term(models.Model):
    term = models.CharField(max_length=100)
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    termNote = models.TextField()
    usage = models.TextField()
    lexeme = models.ForeignKey('lex.Lexeme', related_name='relatedTerm')

