from lex.models import Language, Lexeme, LexicalClass,\
    Form, Representation, RepresentationType, Feature, \
    FeatureValue
from django.contrib import admin

admin.site.register(Language)
admin.site.register(LexicalClass)
admin.site.register(Form)
admin.site.register(Feature)
admin.site.register(FeatureValue)
admin.site.register(Lexeme)
admin.site.register(Representation)
admin.site.register(RepresentationType)
