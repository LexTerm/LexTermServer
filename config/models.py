from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)
    langCode = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class LexicalClass(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

class Form(models.Model):
    name = models.CharField(max_length=100)
    principle = models.BooleanField()
    lexicalClass = models.ForeignKey(LexicalClass, related_name='lexicalClass')
    derivedLexicalClass = models.OneToOneField(LexicalClass, primary_key=False)

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
    enum = models.ForeignKey(Enumeration)

    def __unicode__(self):
        return "%s:%s" % (self.enum, self.name)

class Feature(models.Model):
    name = models.CharField(max_length=100)
    lexicalClass = models.ForeignKey(LexicalClass)
    values = models.ForeignKey(Enumeration)

    def __unicode__(self):
        return self.name

class PreferredLemma(models.Model):
    lexicalClass = models.ForeignKey(LexicalClass)
    form = models.ForeignKey(Form)
    preference = models.IntegerField()

    def __unicode__(self):
        return "preferred_lemma:%s:#%d:%s" % (self.lexicalClass, self.preference, self.form)

class FormValue(models.Model):
    form = models.ForeignKey(Form)
    feature = models.ForeignKey(Feature)
    value = models.ForeignKey(EnumValue)

    def __unicode__(self):
        return "%s:%s:%s" % (self.form, self.feature, self.value)

