from rest_framework.decorators import link
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from lex.models import Language, LexicalClass, Lexeme, \
    Form, FeatureValue, Feature, Representation, RepresentationType, \
    Collection
from lex.serializers import LanguageSerializer, LexicalClassSerializer, \
    LexemeSerializer, FormSerializer, FeatureValueSerializer, \
    FeatureSerializer, RepresentationSerializer, RepresentationTypeSerializer,\
    CollectionSerialzer
from lex.filters import LanguageFilter, LexicalClassFilter, LexemeFilter, \
    FormFilter, FeatureValueFilter, FeatureFilter, RepresentationFilter, \
    RepresentationTypeFilter, CollectionFilter


class LanguageView(ModelViewSet):
    """
    The Language resource accesses the Language model.
    """
    model = Language
    serializer_class = LanguageSerializer
    filter_class = LanguageFilter

    @link()
    def lexemes(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.lexemes)

    @link()
    def representation_types(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.representation_types)


class LexicalClassView(ModelViewSet):
    model = LexicalClass
    serializer_class = LexicalClassSerializer
    filter_class = LexicalClassFilter

    @link()
    def forms(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.forms)

    @link()
    def features(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.features)


class LexemeView(ModelViewSet):
    model = Lexeme
    serializer_class = LexemeSerializer
    filter_class = LexemeFilter

    @link()
    def forms(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.forms.all())


class FormView(ModelViewSet):
    model = Form
    serializer_class = FormSerializer
    filter_class = FormFilter


class FeatureValueView(ModelViewSet):
    model = FeatureValue
    serializer_class = FeatureValueSerializer
    filter_class = FeatureValueFilter


class FeatureView(ModelViewSet):
    model = Feature
    serializer_class = FeatureSerializer
    filter_class = FeatureFilter


class RepresentationView(ModelViewSet):
    model = Representation
    serializer_class = RepresentationSerializer
    filter_class = RepresentationFilter


class RepresentationTypeView(ModelViewSet):
    model = RepresentationType
    serializer_class = RepresentationTypeSerializer
    filter_class = RepresentationTypeFilter


class CollectionView(ModelViewSet):
    model = Collection
    serializer_class = CollectionSerialzer
    filter_class = CollectionFilter
