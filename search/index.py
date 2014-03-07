from elasticutils import get_es
from lex.models import *
from term.models import *

es = get_es()

es.indices.create(
    index='ltm-entries',
    body={
        'mappings': {
            'entry': {
                'id': {'type': 'integer'},
                'lex_id': {'type': 'string'},
                'language': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'lang_code': {'type': 'string'},
                    'region_code': {'type': 'string'}
                },
                'lexical_class': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'}
                },
                'concept': {
                    'id': {'type': 'integer'},
                    'concept_id': {'type': 'string'},
                    'definition': {'type': 'string'},
                    'subject_fields': {
                        'type': 'nested',
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    }
                },
                'collections': {
                    'type': 'nested',
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'}
                },
                'notes': {
                    'type': 'nested',
                    'id': {'type': 'integer'},
                    'note': {'type': 'string'},
                    'note_type': {'type': 'string'}
                },
                'lexical_forms': {
                    'type': 'nested',
                    'id': {'type': 'integer'},
                    'is_lemma': {'type': 'boolean'},
                    'representations': {
                        'type': 'nested',
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'representation_type': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'}
                        }
                    },
                    'forms': {
                        'type': 'nested',
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'features': {
                            'type': 'nested',
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'feature': {
                                'type': 'nested',
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
)


def index_entries(lexemes):
    entries = [{
        
        } for lex in lexemes]
    pass

