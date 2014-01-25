import uuid
from django.db import models
from rest_framework.reverse import reverse

# class TermBase(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __unicode__(self):
#         return self.name


class SubjectField(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self, request):
        return reverse(
            'subject_detail',
            request=request,
            kwargs={'name': self.name})

    def __unicode__(self):
        return u"SubjectField<{}>".format(self.id)


# Concepts are roughly equivalent to TBX's "termEntry" element
class Concept(models.Model):
    concept_id = models.CharField(max_length=100, unique=True, blank=True)
    subjectFields = models.ManyToManyField(SubjectField)
    definition = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.concept_id:
            self.concept_id = uuid.uuid4().hex[:8]
        super(Concept, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Concept<{}>".format(self.id)


class Note(models.Model):
    lexeme = models.ForeignKey('lex.Lexeme', related_name='notes')
    note_type = models.CharField(max_length=100)
    note = models.TextField()
