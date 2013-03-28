from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)

class LexicalClass(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

class Form(models.Model):
    name = models.CharField(max_length=100)
    principle = models.BooleanField()
    lexicalClass = models.ForeignKey(LexicalClass, related_name='lexicalClass')
    derivedLexicalClass = models.OneToOneField(LexicalClass, primary_key=False)

class Representation(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

class Enumeration(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language)

class EnumValue(models.Model):
    name = models.CharField(max_length=100)
    enum = models.ForeignKey(Enumeration)

class Feature(models.Model):
    name = models.CharField(max_length=100)
    lexicalClass = models.ForeignKey(LexicalClass)
    values = models.ForeignKey(Enumeration)

class PreferredLemma(models.Model):
    lexicalClass = models.ForeignKey(LexicalClass)
    form = models.ForeignKey(Form)
    preference = models.IntegerField()

class FormValue(models.Model):
    form = models.ForeignKey(Form)
    feature = models.ForeignKey(Feature)
    value = models.ForeignKey(EnumValue)

