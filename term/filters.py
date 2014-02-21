from rest_framework_chain import ChainedFilterSet, RelatedFilter, \
    AllLookupsFilter
from term.models import Concept, Note, SubjectField


class SubjectFieldFilter(ChainedFilterSet):
    name = AllLookupsFilter(name='name')
    concepts = RelatedFilter('term.filters.ConceptFilter', name='concepts')

    class Meta:
        model = SubjectField


class ConceptFilter(ChainedFilterSet):
    concept_id = AllLookupsFilter(name='concept_id')
    definition = AllLookupsFilter(name='definition')
    subject_fields = RelatedFilter(SubjectFieldFilter, name='subject_fields')
    lexemes = RelatedFilter(
        'lex.filters.LexemeFilter', name='lexemes', distinct=True)

    class Meta:
        model = Concept


class NoteFilter(ChainedFilterSet):
    note = AllLookupsFilter(name='note')
    note_type = AllLookupsFilter(name='note_type')
    lexeme = RelatedFilter('lex.filters.LexemeFilter', name='lexeme')

    class Meta:
        model = Note
