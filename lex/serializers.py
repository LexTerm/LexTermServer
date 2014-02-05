from rest_framework.serializers import ModelSerializer
from lex.models import Language, Lexeme, LexicalClass, \
    Feature, FeatureValue, Form, Representation, RepresentationType, \
    Collection
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
            'id', 'lex_id', 'lex_class',
            'concept', 'forms', 'notes', 'collections')


class FeatureSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'values')


class FeatureValueSerializer(ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ('id', 'name', 'feature', 'forms')


class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = (
            'id', 'name', 'is_lemma', 'lexeme', 'features', 'representations')


class RepresentationSerializer(ModelSerializer):
    class Meta:
        model = Representation
        fields = ('id', 'name', 'form', 'representation_type')


class RepresentationTypeSerializer(ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('id', 'name', 'language', 'representations')


class CollectionSerialzer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'lexemes')
