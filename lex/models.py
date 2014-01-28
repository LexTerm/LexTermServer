import uuid
from django.db import models

#class FormFeatureManager(models.RelatedManager):

    #def add(self, *args, **kwargs


class Language(models.Model):
    """
    The Language model represents a given language such as
    British English en_US. The class currently supports up to
    ISO 63906 and ISO 3166 for language and region codes.

    The Language class has shortcuts to other related models
    such as lexemes, features, and representation_types.
    """

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
    """
    The LexicalClass model represents any possible lexical class such
    as traditional parts of speech (e.g. noun, verb, adjective).
    """
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, related_name="lexical_classes")

    class Meta:
        verbose_name_plural = "Lexical Classes"
        unique_together = ('name', 'language')

    @property
    def forms(self):
        return Form.objects.filter(lexeme__lex_class=self)

    @property
    def features(self):
        return Feature.objects.filter(values__forms__lexeme__lex_class=self)

    def __unicode__(self):
        return "LexicalClass<{}: {}>".format(self.language.locale, self.name)


class Lexeme(models.Model):
    """
    Lexemes are the entries in the lexicon. It should be noted that
    terms are usually described by a lemma, or the prefferred Form of
    a particular lexeme.

    Lexemes have a unique id independent of their row indentifier in
    the database. A Lexeme is described by a particular lexical class
    (which implies a particular language) and a particular concept.
    """

    lex_id = models.CharField(max_length=100, unique=True, blank=True)
    lex_class = models.ForeignKey(LexicalClass, related_name="lexemes")
    concept = models.ForeignKey('term.Concept', related_name='lexemes')

    @property
    def language(self):
        return self.lex_class.language

    def save(self, *args, **kwargs):
        if not self.lex_id:
            self.lex_id = uuid.uuid4().hex[:8]
        super(Lexeme, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.lemma:
            return "Lexeme<{}: {}-{}>".format(
                self.language.locale,
                self.id,
                self.lemma)
        return "Lexeme<{}: {}>".format(self.language.locale, self.id)


class Feature(models.Model):
    """
    The Feature model represents possible features of a language,
    such as Number, Gender, or Case.
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Feature<{}>".format(self.name)


class FeatureValue(models.Model):
    """
    Each feature takes an enumerated set of values. For example,
    the feature Number in English would take the values: Singular
    and Plural.
    """

    name = models.CharField(max_length=100)
    feature = models.ForeignKey(Feature, related_name='values')

    class Meta:
        verbose_name_plural = "Feature Values"
        unique_together = ('name', 'feature')

    def __unicode__(self):
        return "FeatureValue<{}>".format(self.name)


class Form(models.Model):
    """
    Forms are defined by a particular set of Feature Values. Forms should
    be thought of as instances of a type represented by the combination of
    their feature values. They are instances because they are attached to
    a particular lexeme.

    For example, a form defined by the value "singular" and attached to the
    lexeme of the concept of a cat as a noun in English would have a written
    representation of "cat". Likewise, a form with the value "singular" in
    a different language, with a different concept, would have a different
    representation. In fact the structure of the data is such that it would be
    a different form instance even though it has the same feature set. This
    is because forms are subordinate to lexemes in this structure.

    However, becuase FeatureValues do not require a lexeme, it is possible to
    present users with the abstract type "singluar" that they may select for
    a particular form. Those not aware of the structure of the database might
    not actually realize that "singluar" is not what this model describes.

    In previous versions of LexTerm, this was called a LexicalForm.
    """
    #TODO: require that a form not have more than one value for a feature

    # name does not define the form, instead it is defined by the features
    # name is a label for the form chosen by the lexicographer it could be
    # "FORMX123" instead of "1st person plural"
    name = models.CharField(max_length=100)
    # features are instances (values) of the features that the form uses
    features = models.ManyToManyField(FeatureValue, related_name="forms")
    lexeme = models.ForeignKey(Lexeme, related_name='forms')
    is_lemma = models.BooleanField()

    @property
    def lex_class(self):
        return self.lexeme.lex_class

    def clean(self):
        from django.core.exceptions import ValidationError
        # make sure that each feature has only one value
        if len(self.features.all()) != len(Feature.objects.filter(
                values__forms=self).distinct()):
            raise ValidationError('Duplicate feature value in {}'.format(self))

    def save(self, *args, **kwargs):
        # if necessary toggle lemma status
        if self.is_lemma:
            try:
                lemma = Form.objects.get(is_lemma=True, lexeme=self.lexeme)
                if self != lemma:
                    lemma.is_lemma = False
                    lemma.save()
            except Form.DoesNotExist:
                pass
        super(Form, self).save()

    def __unicode__(self):
        return "Form<{}:({}) {}>".format(
            self.lex_class.language.locale,
            self.lex_class.name,
            self.name)


class RepresentationType(models.Model):
    """
    The RepresentationType model stores possible representations for forms.
    There are many different ways of representing a particular form of
    a lexeme. When dealing with terminology, the default is the written
    representation, but even writing may be broken down into various
    systems.
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Representation Types"

    def __unicode__(self):
        return "RepresentationType<{}>".format(self.name)


class Representation(models.Model):
    """
    The Representation model provides instances of representation_types
    for particular forms.
    """
    form = models.ForeignKey(Form, related_name="representations")
    representation_type = models.ForeignKey(
        RepresentationType,
        related_name="representations")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('form', 'representation_type',)

    def __unicode__(self):
        return "Representation<{}: {}>".format(
            self.representation_type.name,
            self.name)
