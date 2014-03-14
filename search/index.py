from django.forms.models import model_to_dict as mtd
from elasticsearch import Elasticsearch
from term.models import *

es = Elasticsearch()

def create_index():
    es.indices.create(
        index='ltm-entries',
        body={
            'mappings': {
                'entry': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'lex_id': {'type': 'string'},
                        'lexical_class': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'language': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'lang_code': {'type': 'string'},
                                        'region_code': {'type': 'string'},
                                        'locale': {'type': 'string'}
                                    }
                                }
                            }
                        },
                        'concept': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'concept_id': {'type': 'string'},
                                'definition': {'type': 'string'},
                                'subject_fields': {
                                    'type': 'nested',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'}
                                    }
                                }
                            }
                        },
                        'collections': {
                            'type': 'nested',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        },
                        'notes': {
                            'type': 'nested',
                            'properties': {
                                'id': {'type': 'integer'},
                                'note': {'type': 'string'},
                                'note_type': {'type': 'string'}
                            }
                        },
                        'lexical_forms': {
                            'type': 'nested',
                            'properties': {
                                'id': {'type': 'integer'},
                                'is_lemma': {'type': 'boolean'},
                                'representations': {
                                    'type': 'nested',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'representation_type': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            },
                            'form': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer'},
                                    'name': {'type': 'string'},
                                    'features': {
                                        'type': 'nested',
                                        'properties': {
                                            'id': {'type': 'integer'},
                                            'name': {'type': 'string'},
                                            'feature': {
                                                'type': 'object',
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )

def index_entries(lexemes):
    for lex in lexemes:
        entry = mtd(lex)
        lex_class = mtd(lex.lexical_class)
        lang = mtd(lex.lexical_class.language)
        lang['locale'] = lex.lexical_class.language.locale
        lex_class['language'] = lang
        entry['lexical_class'] = lex_class
        concept = mtd(lex.concept)
        for ind, subid in enumerate(concept['subject_fields']):
            concept['subject_fields'][ind] = mtd(lex.concept.subject_fields.get(id=subid))
        entry['concept'] = concept
        entry['collections'] = []
        for col in lex.collections.all():
            col_dict = mtd(col)
            col_dict.pop('lexemes')
            entry['collections'].append(col_dict)
        entry['notes'] = [mtd(col) for col in lex.notes.all()]
        entry['lexical_forms'] = []
        for lex_form in lex.lexical_forms.all():
            lex_form_dict = mtd(lex_form)
            lex_form_dict.pop('lexeme')
            lex_form_dict['representations'] = []
            for rep in lex_form.representations.all():
                rep_dict = mtd(rep)
                rep_type = mtd(rep.representation_type)
                rep_dict['representation_type'] = rep_type
                lex_form_dict['representations'].append(rep_dict)

            form = mtd(lex_form.form)
            form.pop('lexemes')
            for ind, vid in enumerate(form['features']):
                value = lex_form.form.features.get(id=vid)
                value_dict = mtd(value)
                feature = mtd(value.feature)
                value_dict['feature'] = feature
                form['features'][ind] = value_dict
            lex_form_dict['form'] = form
            entry['lexical_forms'].append(lex_form_dict)
        es.index(body=entry, id=lex.id, index='ltm-entries', doc_type='entry', refresh=True)

def rebuild_index():
    # avoid circular import
    from lex.models import Lexeme
    es.indices.delete(index="_all")
    create_index()
    index_entries(Lexeme.objects.all())

try:
    create_index()
except:
    # index should already exist
    pass
