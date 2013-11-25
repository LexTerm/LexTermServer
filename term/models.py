from django.db import models
from term.fields import UUIDField
# from lex.models import Language, Lexeme

# class TermBase(models.Model):
#     name = models.CharField(max_length=100)
# 
#     def __unicode__(self):
#         return self.name

class SubjectField(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# Concepts are roughly equivalent to TBX's "termEntry" element
class Concept(models.Model):
    # name = models.CharField(max_length=100) # should be an id, not a name
    id = UUIDField(primary_key=True, auto=True, short=True)
    subjectFields = models.ManyToManyField(SubjectField)
    definition = models.TextField(blank=True)
    # termBase = models.ForeignKey(TermBase)
    # superOrdinate = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.id

# class ConceptDefinition(models.Model):
#     concept = models.ForeignKey(Concept)
#     language = models.ForeignKey('lex.Language')
#     definition = models.TextField()
# 
#     def __unicode__(self):
#         return "definition: %s: %s" % (self.concept, self.language)

# Try merging lexeme and term
# class Term(models.Model):
#     term = models.CharField(max_length=100)
#     concept = models.ForeignKey(Concept)
#     language = models.ForeignKey('lex.Language')
#     termNote = models.TextField()
#     usage = models.TextField()
#     lexeme = models.ForeignKey('lex.Lexeme', related_name='relatedTerm')
# 
#     def __unicode__(self):
#         return self.term
# 
