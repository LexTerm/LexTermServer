from django.forms import widgets
from rest_framework.serializers import *
from lex.models import *
import logging
logger = logging.getLogger(__name__)

# Serializers for Lex API

class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ('name', 'langCode')

    def to_native(self, obj):
        if not obj:
            return
        ret = super(LanguageSerializer, self).to_native(obj)
        ret['_links'] = {
            'self': obj.get_absolute_url(self.context['request']),
            'lexemes': reverse('lexeme_list', request=self.context['request'], 
                kwargs={'langCode':obj.langCode}),
        }
        return ret

class LexemeSerializer(ModelSerializer):
    class Meta:
        model = Lexeme
        fields = ('id', 'lemma')

    def to_native(self, obj):
        if not obj:
            return
        ret = super(LexemeSerializer, self).to_native(obj)
        ret['_links'] = {
            'self': obj.get_absolute_url(self.context['request']),
            'forms': reverse('lexical_form_list', request=self.context['request'], 
                kwargs={'langCode':obj.language.langCode, 'id':obj.id}),
        }
        return ret

class LexicalFormSerializer(ModelSerializer):
    class Meta:
        model = LexicalForm
        fields = ('representation',)

    def to_native(self, obj):
        if not obj:
            return
        ret = super(LexicalFormSerializer, self).to_native(obj)
        ret['_links'] = {
            'self': obj.get_absolute_url(self.context['request']),
            'form': "not implemented",
            'lexeme': "not implemented"
        }
        return ret

class LexicalClassSerializer(ModelSerializer):
    class Meta:
        model = LexicalClass
        fields = ('name', 'language')

# class EnumValueSerializer(Serializer):
#     value = CharField(max_length=100)
# 
#     def restore_object(self, attrs, instance=None):
#         if instance is not None:
#             instance.value = attrs.get('value', instance.value)
#             return instance
#         return EnumValue(**attrs)

class EnumValueSerializer(ModelSerializer):
    class Meta:
        model = EnumValue
        fields = ('value', 'enum')

class EnumSerializer(ModelSerializer):
    # def get_related_field(self, model_field, related_model, to_many):
    #     kwargs = {
    #         'queryset': related_model.objects.filter(enum=model_field.name),
    #         'many': to_many
    #     }
    # name = CharField()
    # qset = EnumValue.objects.filter(enum=name)
    # values = SlugRelatedField(many=True, slug_field='value')
    values = RelatedField(many=True)
    # values = EnumValueSerializer(many=True) # requires posting values with enum

    class Meta:
        model = Enumeration
        fields = ('name', 'language', 'values')

# class EnumListSerializer(Serializer):
#     def to_native(self, obj):
#         if not obj:
#             return {}
#         logger.info("obj: "+str(obj))
#         return str(obj)

class EnumListSerializer(ModelSerializer):
    class Meta:
        model = Enumeration
        fields = ('name',)

class RepTypeSerializer(ModelSerializer):
    class Meta:
        model = RepresentationType
        fields = ('name', 'language')

class FormSerializer(ModelSerializer):
    values = RelatedField(many=True)

    class Meta:
        model = Form
        fields = ('name', 'lexicalClass', 'values')

# class LexicalClassSerializer(ModelSerializer):
#     class Meta:

