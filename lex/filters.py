from rest_framework.filters import BaseFilterBackend

# We are doing filtering like this because it is based on multiple parameters from the urlconf

class LanguageFilter(BaseFilterBackend):
    """
    Filters querysets based on language
    """
    def filter_queryset(self, request, queryset, view):
        lang = view.kwargs['lang']
        return queryset.filter(language=lang)

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

