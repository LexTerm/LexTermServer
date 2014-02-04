from rest_framework.serializers import ModelSerializer
from lex.models import Language, Lexeme, LexicalClass, \
    Feature, FeatureValue, Form, Representation, RepresentationType, \
    Collection
import logging
logger = logging.getLogger(__name__)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'region_code', 'name')


class LexicalClassSerializer(ModelSerializer):
    class Meta:
        model = LexicalClass
        fields = ('id', 'name', 'language')


class LexemeSerializer(ModelSerializer):
    class Meta:
        model = Lexeme
        fields = ('id', 'lex_id', 'lex_class', 'concept')


class FeatureSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name')


class FeatureValueSerializer(ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ('id', 'name', 'feature')


class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = ('id', 'name', 'is_lemma', 'lexeme', 'features')


class RepresentationSerializer(ModelSerializer):
    class Meta:
        model = Representation
        fields = ('id', 'name', 'form', 'representation_type')


class RepresentationTypeSerializer(ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('id', 'name', 'language')


class CollectionSerialzer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'lexemes')
