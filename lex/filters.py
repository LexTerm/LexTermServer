from rest_framework.filters import BaseFilterBackend
from lex.models import *

# We are doing filtering like this because it is based on multiple parameters from the urlconf

class LanguageFilter(BaseFilterBackend):
    """
    Filters querysets based on language
    """
    def filter_queryset(self, request, queryset, view):
        lang = view.kwargs['langCode']
        return queryset.filter(language=lang)

class EnumFilter(BaseFilterBackend):
    """
    Filters querysets based on enumeration and language
    """
    def filter_queryset(self, request, queryset, view):
        lang = view.kwargs['langCode']
        enumName = view.kwargs['name']
        enum = Enumeration.objects.get(language=lang, name=enumName)
        return queryset.filter(enum=enum)

class LexemeFilter(BaseFilterBackend):
    """
    Filters querysets based on lexeme and language
    """
    def filter_queryset(self, request, queryset, view):
        lang = view.kwargs['langCode']
        lexId = view.kwargs['id']
        lexeme = Lexeme.objects.get(language=lang, id=lexId)
        return queryset.filter(lexeme=lexeme)

class NameFilter(BaseFilterBackend):
    """
    Filters querysets based on a name field, if the field was provided
    """
    def filter_queryset(self, request, queryset, view):
        if 'name' in view.kwargs:
            name = view.kwargs['name']
            return queryset.filter(name=name)
        else:
            return queryset

class IDFilter(BaseFilterBackend):
    """
    Filters querysets based on an id field, if the field was provided
    """
    def filter_queryset(self, request, queryset, view):
        if 'id' in view.kwargs:
            search_id = view.kwargs['id']
            return queryset.filter(id=search_id)
        else:
            return queryset

