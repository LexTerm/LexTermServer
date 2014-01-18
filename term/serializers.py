from rest_framework.serializers import ModelSerializer, RelatedField
from term.models import SubjectField, Concept

# Serializers for termbase API


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = SubjectField
        fields = ('name',)

    def to_native(self, obj):
        if not obj:
            return
        ret = super(SubjectSerializer, self).to_native(obj)
        ret['_links'] = {
            'self': obj.get_absolute_url(self.context['request'])
        }
        return ret


class ConceptSerializer(ModelSerializer):
    subjectFields = RelatedField(many=True)

    class Meta:
        model = Concept
        fields = ('id', 'subjectFields', 'definition')

# class LexemeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LexemeTerm
#         fields = ('name', 'language', 'concept', 'termNote', 'usage')
#
