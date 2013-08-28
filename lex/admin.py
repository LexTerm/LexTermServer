from lex.models import *
from django.contrib import admin

admin.site.register(Language)
admin.site.register(LexicalClass)
admin.site.register(Form)

class RepTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')
admin.site.register(RepresentationType, RepTypeAdmin)

class EnumValueInline(admin.TabularInline):
    model = EnumValue
    extra = 3

class EnumerationAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')
    inlines = [EnumValueInline]
admin.site.register(Enumeration, EnumerationAdmin)

class EnumValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'enum', 'language')
admin.site.register(EnumValue, EnumValueAdmin)

admin.site.register(Feature)
admin.site.register(PreferredLemma)
admin.site.register(FormValue)
admin.site.register(LexemeTerm)
admin.site.register(Representation)
admin.site.register(PartOfSpeech)
admin.site.register(FeatureSet)
admin.site.register(WordSense)

