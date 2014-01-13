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
