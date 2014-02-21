from rest_framework.serializers import ModelSerializer
from lex.models import Language, Lexeme, LexicalClass, \
    Feature, FeatureValue, Form, Representation, RepresentationType, \
    Collection, LexicalForm
import logging
logger = logging.getLogger(__name__)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'region_code', 'name', 'lexical_classes')


class LexicalClassSerializer(ModelSerializer):
    class Meta:
        model = LexicalClass
        fields = ('id', 'name', 'language', 'lexemes')


class LexemeSerializer(ModelSerializer):
    class Meta:
        model = Lexeme
        fields = (
            'id', 'lex_id', 'lexical_class',
            'concept')  #, 'forms', 'lexical_forms', 'notes', 'collections')


class LexicalFormSerializer(ModelSerializer):
    class Meta:
        model = LexicalForm
        fields = ('id', 'lexeme', 'form', 'is_lemma', 'representations')


class FeatureSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'featurevalues')


class FeatureValueSerializer(ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ('id', 'name', 'feature', 'forms')


class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = (
            'id', 'name', 'lexemes', 'lexical_forms', 'features')


class RepresentationSerializer(ModelSerializer):
    class Meta:
        model = Representation
        fields = ('id', 'name', 'lexical_form', 'representation_type')


class RepresentationTypeSerializer(ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('id', 'name', 'representations')


class CollectionSerialzer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'lexemes')
