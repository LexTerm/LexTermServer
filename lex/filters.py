from rest_framework.filters import BaseFilterBackend

class LanguageFilter(BaseFilterBackend):
    """
    Filters querysets based on language
    """
    def filter_queryset(self, request, queryset, view):
        lang = view.kwargs['lang']
        return queryset.filter(language=lang)

class NameFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'name' in view.kwargs:
            name = view.kwargs['name']
            return queryset.filter(name=name)
        else:
            return queryset
