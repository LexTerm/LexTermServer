from rest_framework.filters import BaseFilterBackend

# We are doing filtering like this because it is based on multiple parameters from the urlconf

class SubjectFilter(BaseFilterBackend):
    """
    Filters querysets based on subject, if present
    """
    def filter_queryset(self, request, queryset, view):
        if 'subject' in view.kwargs:
            subj = view.kwargs['subject']
            return queryset.filter(subject=subj)
        else:
            return queryset

