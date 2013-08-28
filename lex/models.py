from django.db import models
# from term.models import Term

class Language(models.Model):
    langCode = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('langCode',)

class LexicalClass(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

class Form(models.Model):
    name = models.CharField(max_length=100)
    principle = models.BooleanField()
    lexicalClass = models.ForeignKey(LexicalClass, related_name='lexicalClass')
    derivedLexicalClass = models.OneToOneField(LexicalClass)

    def __unicode__(self):
        return self.name

class RepresentationType(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

class Enumeration(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

class EnumValue(models.Model):
    name = models.CharField(max_length=100)
    enum = models.ForeignKey(Enumeration, related_name='values')

    def language(self):
        return self.enum.language.__unicode__()

    def __unicode__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100)
    lexicalClass = models.ForeignKey(LexicalClass, related_name='features')
    values = models.ForeignKey(Enumeration)

    def __unicode__(self):
        return self.name

class PreferredLemma(models.Model):
    lexicalClass = models.ForeignKey(LexicalClass, related_name='preferred_lemmas')
    form = models.ForeignKey(Form)
    preference = models.IntegerField()

    def __unicode__(self):
        return "preferred_lemma:%s:#%d:%s" % (self.lexicalClass, self.preference, self.form)

class FormValue(models.Model):
    form = models.ForeignKey(Form, related_name='values')
    feature = models.ForeignKey(Feature)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s:%s" % (self.form, self.feature, self.value)

# Merging Term and Lexeme
class LexemeTerm(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)
    # term = models.ForeignKey('term.Term', related_name='relatedLexeme')
    concept = models.ForeignKey('term.Concept', blank=True, null=True)
    termNote = models.TextField(blank=True)
    usage = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Representation(models.Model):
    lexeme = models.ForeignKey(LexemeTerm)
    representationType = models.ForeignKey(RepresentationType)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class PartOfSpeech(models.Model):
    lexeme = models.ForeignKey(LexemeTerm)
    lexicalClass = models.ForeignKey(LexicalClass)

    def __unicode__(self):
        return self.lexicalClass

class FeatureSet(models.Model):
    lexeme = models.ForeignKey(LexemeTerm)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s" % (self.lexeme, self.value)

class WordSense(models.Model):
    lexeme = models.ForeignKey(LexemeTerm)
    concept = models.ForeignKey('term.Concept')
    etymology = models.TextField()
    
    def __unicode__(self):
        return "%s:%s" % (self.lexeme, self.concept)

