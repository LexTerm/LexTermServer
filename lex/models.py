from django.db import models
from rest_framework.reverse import reverse
from term.fields import UUIDField


class Language(models.Model):
    langCode = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self, request):
        return reverse('language_detail', request=request, kwargs={'langCode': self.langCode})

    class Meta:
        ordering = ('langCode',)


class LexicalClass(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'language')


class Form(models.Model):
    name = models.CharField(max_length=100)
    lexicalClass = models.ForeignKey(LexicalClass, related_name='forms')
    preference = models.IntegerField()
    # principle = models.BooleanField()
    # derivedLexicalClass = models.OneToOneField(LexicalClass)

    def __unicode__(self):
        return "{}-{}".format(self.lexicalClass, self.name)

    class Meta:
        ordering = ('preference',)
        unique_together = ('name', 'lexicalClass')


class Enumeration(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'language')


class EnumValue(models.Model):
    value = models.CharField(max_length=100)
    enum = models.ForeignKey(Enumeration, related_name='values')

    def language(self):
        # return self.enum.language.__unicode__()
        return self.enum.language

    def __unicode__(self):
        return self.value

    class Meta:
        unique_together = ('value', 'enum')


class Feature(models.Model):
    name = models.CharField(max_length=100)
    lexicalClass = models.ForeignKey(LexicalClass, related_name='features')
    values = models.ForeignKey(Enumeration)

    def __unicode__(self):
        return self.name


class FormValue(models.Model):
    form = models.ForeignKey(Form, related_name='values')
    feature = models.ForeignKey(Feature)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s:%s" % (self.form, self.feature, self.value)

# Merging Term and Lexeme


class Lexeme(models.Model):
    id = UUIDField(primary_key=True, auto=True, short=True)
    language = models.ForeignKey(Language)
    lexicalClass = models.ForeignKey(LexicalClass)
    concept = models.ForeignKey(
        'term.Concept', blank=True, null=True, related_name='terms')
    lemma = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        if self.lemma:
            return "{}({})".format(self.id, self.lemma)
        return "{}".format(self.id)

    def get_absolute_url(self, request):
        return reverse('lexeme_detail', request=request,
                       kwargs={'langCode': self.language.langCode, 'id': self.id})


class TermNote(models.Model):
    lexeme = models.ForeignKey(Lexeme, related_name='term_notes')
    type = models.CharField(max_length=100)
    note = models.TextField()


class LexicalForm(models.Model):
    lexeme = models.ForeignKey(Lexeme, related_name='forms')
    form = models.ForeignKey(Form)
    representation = models.CharField(max_length=200)

    def __unicode__(self):
        return self.representation

    def get_absolute_url(self, request):
        return reverse('lexical_form_detail', request=request,
                       kwargs={'langCode': self.lexeme.language.langCode,
                               'id': self.lexeme.id, 'form': self.form.name})

    class Meta:
        unique_together = ('lexeme', 'form')

    # recalculate the lexeme's lemma every time we save a lexical form
    def save(self, *args, **kwargs):
        super(LexicalForm, self).save(*args, **kwargs)
        pref_forms = Form.objects.filter(lexicalform__lexeme=self.lexeme)
        cur_forms = LexicalForm.objects.filter(lexeme=self.lexeme)
        # preferred forms are already ordered by preference
        for pform in pref_forms:
            for cform in cur_forms:
                if cform.form == pform:
                    self.lexeme.lemma = cform.representation
                    self.lexeme.save()
                    return


class RepresentationType(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'language')


class Representation(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    representationType = models.ForeignKey(RepresentationType)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class FeatureSet(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s" % (self.lexeme, self.value)
