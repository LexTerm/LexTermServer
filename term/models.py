from django.db import models
from term.fields import UUIDField
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
