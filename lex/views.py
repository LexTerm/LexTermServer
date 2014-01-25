from rest_framework.decorators import link
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from lex.models import Language, LexicalClass, Lexeme, \
    Form, FeatureValue, Feature, Representation, RepresentationType


class LanguageView(ModelViewSet):
    model = Language
    #serializer_class = LanguageSerializer

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
    #serializer_class = LexicalClassSerializer

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
    #serializer_class = LexemeSerializer

    @link()
    def forms(self, request, pk=None):
        obj = self.get_object()
        return Response(obj.forms.all())


class FormView(ModelViewSet):
    model = Form


class FeatureValueView(ModelViewSet):
    model = FeatureValue


class FeatureView(ModelViewSet):
    model = Feature


class RepresentationView(ModelViewSet):
    model = Representation


class RepresentationTypeView(ModelViewSet):
    model = RepresentationType
