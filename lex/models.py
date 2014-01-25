import uuid
from django.db import models


class Language(models.Model):
    # ISO 639-6 is the current longest possible code
    lang_code = models.CharField(max_length=4)
    # ISO 3166-1 alpha-3 is the current longest code
    region_code = models.CharField(max_length=3, blank=True, default='')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('lang_code', 'region_code',)
        ordering = ('lang_code',)

    @property
    def locale(self):
        return self.lang_code + "_" + self.region_code

    @property
    def lexemes(self):
        return Lexeme.objects.filter(lex_class__language=self)

    @property
    def features(self):
        return Feature.objects.filter(
            values__forms__lexeme__lex_class__language=self)

    @property
    def representation_types(self):
        return RepresentationType.objects.filter(
            representations__form__lexeme__lex_class__language=self)

    def __unicode__(self):
        return "Language<{}>".format(self.locale)


class LexicalClass(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, related_name="lexical_classes")

    @property
    def features(self):
        return Feature.objects.filter(values__forms__lexeme__lex_class=self)

    def __unicode__(self):
        return "LexicalClass<{}: {}>".format(self.language.locale, self.name)

    class Meta:
        unique_together = ('name', 'language')


class Lexeme(models.Model):
    lex_id = models.CharField(max_length=100, unique=True, blank=True)
    lex_class = models.ForeignKey(LexicalClass, related_name="lexemes")
    concept = models.ForeignKey(
        'term.Concept', blank=True, null=True, related_name='lexemes')
    lemma = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.lex_id:
            self.lex_id = uuid.uuid4().hex[:8]
        super(Lexeme, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.lemma:
            return "Lexeme<{}: {}-{}>".format(
                self.lex_class.language.locale,
                self.id,
                self.lemma)
        return "Lexeme<{}: {}>".format(self.lex_class.language.locale, self.id)


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Feature<{}>".format(self.name)


class FeatureValue(models.Model):
    value = models.CharField(max_length=100)
    feature = models.ForeignKey(Feature, related_name='values')

    def __unicode__(self):
        return "FeatureValue<{}>".format(self.value)

    class Meta:
        unique_together = ('value', 'feature')


class Form(models.Model):
    # name does not define the form, instead it is defined by the features
    # name is a label for the form chosen by the lexicographer it could be
    # "FORMX123" instead of "1st person plural"
    name = models.CharField(max_length=100)
    # features are instances (values) of the features that the form uses
    features = models.ManyToManyField(FeatureValue, related_name="forms")
    lexeme = models.ForeignKey(Lexeme, related_name='forms')
    preference = models.IntegerField()

    @property
    def lex_class(self):
        return self.lexeme.lex_class

    def __unicode__(self):
        return "Form<{}:({}) {}>".format(
            self.lex_class.language.locale,
            self.lex_class.name,
            self.name)

    class Meta:
        ordering = ('preference',)


class RepresentationType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "RepresentationType<{}>".format(self.name)


class Representation(models.Model):
    form = models.ForeignKey(Form, related_name="representations")
    representation_type = models.ForeignKey(
        RepresentationType,
        related_name="representations")
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Representation<{}: {}>".format(
            self.representation_type.name,
            self.name)
