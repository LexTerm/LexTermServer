import uuid
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


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
            values__forms__lexemes__lex_class__language=self)

    @property
    def representation_types(self):
        return RepresentationType.objects.filter(
            representations__lexical_form__lexeme__lex_class__language=self)

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
        return Form.objects.filter(lexemes__lex_class=self)

    @property
    def features(self):
        return Feature.objects.filter(values__forms__lexemes__lex_class=self)

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
    feature = models.ForeignKey(Feature, related_name='featurevalues')

    class Meta:
        verbose_name_plural = "Feature Values"
        unique_together = ('name', 'feature')

    def __unicode__(self):
        return "FeatureValue<{}>".format(self.name)


class Form(models.Model):
    """
    Forms are defined by a particular set of Feature Values.

    :name does not define the form, instead it is defined by the features
    :name is a label for the form chosen by the lexicographer it could be
    "FORMX123" instead of "1st person plural"
    """

    name = models.CharField(max_length=100)
    # features are instances (values) of the features that the form uses
    features = models.ManyToManyField(FeatureValue, related_name="forms")
    lexemes = models.ManyToManyField(
        Lexeme,
        related_name='forms',
        through='LexicalForm')

    @property
    def lexical_classes(self):
        return LexicalClass.objects.filter(lexemes__forms=self)

    def __unicode__(self):
        return "Form<{}>".format(self.name)


class LexicalForm(models.Model):
    """
    This is an intermediary model for storing information about the
    relationship between a lexeme and a form. This information includes whether
    the form is the lemma for the given lexeme and also the representations
    that pertain tothe relationship. This model allows us to avoid duplication
    of forms via lexemes.
    """

    lexeme = models.ForeignKey(Lexeme, related_name="lexical_forms")
    form = models.ForeignKey(Form, related_name="lexical_forms")
    is_lemma = models.BooleanField()

    def save(self, *args, **kwargs):
        # if necessary toggle lemma status
        if self.is_lemma:
            try:
                lemma = LexicalForm.objects.get(
                    is_lemma=True,
                    lexeme=self.lexeme,
                    form=self.form)
                if self != lemma:
                    lemma.is_lemma = False
                    lemma.save()
            except LexicalForm.DoesNotExist:
                pass
        super(LexicalForm, self).save()


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
    lexical_form = models.ForeignKey(
        LexicalForm,
        related_name="representations")
    representation_type = models.ForeignKey(
        RepresentationType,
        related_name="representations")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('lexical_form', 'representation_type',)

    def __unicode__(self):
        return "Representation<{}: {}>".format(
            self.representation_type.name,
            self.name)


class Collection(models.Model):
    """
    A collection of lexemes to help manage portions of the data.
    """
    name = models.CharField(max_length=50)
    lexemes = models.ManyToManyField(Lexeme, related_name="collections")


@receiver(m2m_changed, sender=Form.features.through)
def limit_feature_combinations(sender, **kwargs):
    if kwargs['action'] == "pre_add":
        # clear out any feature values that have the same feature as the new
        for pk in kwargs['pk_set']:
            feature = Feature.objects.get(values__pk=pk)
            for old_value in kwargs['instance'].features.all():
                if old_value.feature == feature:
                    kwargs['instance'].features.remove(old_value)

    if kwargs['action'] == "post_add":
        # sanitize current data
        existing = []
        for value in kwargs['instance'].features.all():
            if value.feature in existing:
                kwargs['instance'].features.remove(value)
            else:
                existing.append(value)
