from django.db import models
from lex.models import *

class TermBase(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class SubjectField(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Concept(models.Model):
    name = models.CharField(max_length=100)
    termBase = models.ForeignKey(TermBase)
    subjectField = models.ManyToManyField(SubjectField)
    superOrdinate = models.ForeignKey('self')

    def __unicode__(self):
        return self.name

class ConceptDefinition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    definition = models.TextField()

    def __unicode__(self):
        return "concept_definition:%s:%s" % (self.concept, self.language)

class Term(models.Model):
    term = models.CharField(max_length=100)
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    termNote = models.TextField()
    usage = models.TextField()
    lexeme = models.ForeignKey(Lexeme, related_name='relatedTerm')

    def __unicode__(self):
        return self.term

