from rest_framework.decorators import link
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from lex.models import Language, LexicalClass, Lexeme, \
    Form, FeatureValue, Feature, Representation, RepresentationType, \
    Collection, LexicalForm
from lex.serializers import LanguageSerializer, LexicalClassSerializer, \
    LexemeSerializer, FormSerializer, FeatureValueSerializer, \
    FeatureSerializer, RepresentationSerializer, RepresentationTypeSerializer,\
    CollectionSerialzer, LexicalFormSerializer, LexicalClassListSerializer, \
    LexemeListSerializer, FormListSerializer, CollectionListSerialzer
from lex.filters import LanguageFilter, LexicalClassFilter, LexemeFilter, \
    FormFilter, FeatureValueFilter, FeatureFilter, RepresentationFilter, \
    RepresentationTypeFilter, CollectionFilter, LexicalFormFilter


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
        serializer = LexemeSerializer(obj.lexemes)
        return Response(serializer.data)

    @link()
    def representation_types(self, request, pk=None):
        obj = self.get_object()
        serializer = RepresentationTypeSerializer(obj.representation_types)
        return Response(serializer.data)

    @link()
    def lexical_classes(self, request, pk=None):
        obj = self.get_object()
        serializer = LexicalClassSerializer(obj.lexical_classes)
        return Response(serializer.data)


class LexicalClassView(ModelViewSet):
    model = LexicalClass
    serializer_class = LexicalClassSerializer
    filter_class = LexicalClassFilter

    def list(self, request):
        query = self.get_queryset()
        query = LexicalClassFilter(request.GET, query)
        serializer = LexicalClassListSerializer(query)
        return Response(serializer.data)

    @link()
    def forms(self, request, pk=None):
        obj = self.get_object()
        serializer = FormSerializer(obj.forms)
        return Response(serializer.data)

    @link()
    def features(self, request, pk=None):
        obj = self.get_object()
        serializer = FeatureSerializer(obj.features)
        return Response(serializer.data)


class LexemeView(ModelViewSet):
    model = Lexeme
    serializer_class = LexemeSerializer
    filter_class = LexemeFilter

    def list(self, request):
        query = self.get_queryset()
        query = LexemeFilter(request.GET, query)
        serializer = LexemeListSerializer(query)
        return Response(serializer.data)

    @link()
    def forms(self, request, pk=None):
        obj = self.get_object()
        serializer = FormSerializer(obj.forms.all())
        return Response(serializer.data)

    @link()
    def lexical_forms(self, request, pk=None):
        obj = self.get_object()
        serializer = LexicalFormSerializer(obj.lexical_forms.all())
        return Response(serializer.data)


class FormView(ModelViewSet):
    model = Form
    serializer_class = FormSerializer
    filter_class = FormFilter

    def list(self, request):
        query = self.get_queryset()
        query = FormFilter(request.GET, query)
        serializer = FormListSerializer(query)
        return Response(serializer.data)


class LexicalFormView(ModelViewSet):
    model = LexicalForm
    serializer_class = LexicalFormSerializer
    filter_class = LexicalFormFilter


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

    def list(self, request):
        query = self.get_queryset()
        query = CollectionFilter(request.GET, query)
        serializer = CollectionListSerialzer(query)
        return Response(serializer.data)
