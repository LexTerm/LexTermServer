from rest_framework_chain import ChainedFilterSet, RelatedFilter, \
    AllLookupsFilter
from lex.models import Language, Lexeme, LexicalClass, \
    Feature, FeatureValue, Form, Representation, RepresentationType, \
    Collection, LexicalForm


class LanguageFilter(ChainedFilterSet):
    lang_code = AllLookupsFilter(name='lang_code')
    region_code = AllLookupsFilter(name='region_code')
    name = AllLookupsFilter(name='name')
    lexical_classes = RelatedFilter(
        'lex.filters.LexicalClassFilter',
        name='lexical_classes')

    class Meta:
        model = Language


class LexicalClassFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    language = RelatedFilter(LanguageFilter, name='language')
    lexemes = RelatedFilter('lex.filters.LexemeFilter', name='lexemes')

    class Meta:
        model = LexicalClass


class LexemeFilter(ChainedFilterSet):
    lex_id = AllLookupsFilter(name='lex_id')
    lex_class = RelatedFilter(LexicalClassFilter, name='lex_class')
    concept = RelatedFilter('term.filters.ConceptFilter', name='concept')
    notes = RelatedFilter('term.filters.NoteFilter', name='notes')
    forms = RelatedFilter(
        'lex.filters.FormFilter',
        name='forms',
        distinct=True)
    collections = RelatedFilter(
        'lex.filters.CollectionFilter',
        name='collections',
        distinct=True)

    class Meta:
        model = Lexeme


class FormFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    lexemes = RelatedFilter(LexemeFilter, name='lexemes')
    features = RelatedFilter('lex.filters.FeatureValueFilter', name='features')

    class Meta:
        model = Form


class FeatureFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    featurevalues = RelatedFilter(
        'lex.filters.FeatureValueFilter',
        name='featurevalues')

    class Meta:
        model = Feature


class FeatureValueFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    feature = RelatedFilter(FeatureFilter, name='feature')
    forms = RelatedFilter(FormFilter, name='forms')

    class Meta:
        model = FeatureValue


class RepresentationFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    lexical_form = RelatedFilter(
        'lex.filters.LexicalFormFilter',
        name='lexical_form')
    representation_type = RelatedFilter(
        'lex.filters.RepresentationTypeFilter',
        name='representation_type')

    class Meta:
        model = Representation


class RepresentationTypeFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    representations = RelatedFilter(
        RepresentationFilter,
        name='representations')

    class Meta:
        model = RepresentationType


class CollectionFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    lexemes = RelatedFilter(
        LexemeFilter,
        name='lexemes',
        distinct=True)

    class Meta:
        model = Collection


class LexicalFormFilter(ChainedFilterSet):
    is_lemma = AllLookupsFilter(name='is_lemma')
    lexeme = RelatedFilter(LexemeFilter, name='lexeme')
    form = RelatedFilter(FormFilter, name='form')
    representations = RelatedFilter(
        RepresentationFilter, name='representations')

    class Meta:
        model = LexicalForm
