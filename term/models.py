import uuid
from django.db import models
from lex.models import Lexeme


class SubjectField(models.Model):
    """
    The SubjectField model represents various domains.
    """

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Subject Fields"

    def get_lexemes(self):
        return Lexeme.objects.filter(concepts__subject_fields=self)

    def __unicode__(self):
        return u"SubjectField<{}>".format(self.id)


# Concepts are roughly equivalent to TBX's "termEntry" element
class Concept(models.Model):
    """
    Concepts correspond to terminological concepts.
    """

    concept_id = models.CharField(max_length=100, unique=True, blank=True)
    subject_fields = models.ManyToManyField(
        SubjectField,
        related_name="concepts")
    definition = models.TextField(blank=True)

    def get_lexemes(self):
        return self.lexemes.all()

    def save(self, *args, **kwargs):
        if not self.concept_id:
            self.concept_id = uuid.uuid4().hex[:8]
        super(Concept, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Concept<{}>".format(self.id)


#TODO: abstract out note_type
class Note(models.Model):
    """
    Notes correspond to termNotes in TBX. This model should only be used
    for those termNotes that are not already represented by other parts
    of the LexTerm system such as LexicalClass.
    """

    lexeme = models.ForeignKey('lex.Lexeme', related_name='notes')
    note_type = models.CharField(max_length=100)
    note = models.TextField()

    def get_lexemes(self):
        return [self.lexeme]
