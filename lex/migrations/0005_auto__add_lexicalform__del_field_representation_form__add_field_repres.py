# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Representation', fields ['form', 'representation_type']
        db.delete_unique(u'lex_representation', ['form_id', 'representation_type_id'])

        # Adding model 'LexicalForm'
        db.create_table(u'lex_lexicalform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexical_forms', to=orm['lex.Lexeme'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexical_forms', to=orm['lex.Form'])),
            ('is_lemma', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'lex', ['LexicalForm'])

        # Deleting field 'Representation.form'
        db.delete_column(u'lex_representation', 'form_id')

        # Adding field 'Representation.lexical_form'
        db.add_column(u'lex_representation', 'lexical_form',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='representations', to=orm['lex.LexicalForm']),
                      keep_default=False)

        # Adding unique constraint on 'Representation', fields ['lexical_form', 'representation_type']
        db.create_unique(u'lex_representation', ['lexical_form_id', 'representation_type_id'])

        # Deleting field 'Form.is_lemma'
        db.delete_column(u'lex_form', 'is_lemma')

        # Deleting field 'Form.lexeme'
        db.delete_column(u'lex_form', 'lexeme_id')


    def backwards(self, orm):
        # Removing unique constraint on 'Representation', fields ['lexical_form', 'representation_type']
        db.delete_unique(u'lex_representation', ['lexical_form_id', 'representation_type_id'])

        # Deleting model 'LexicalForm'
        db.delete_table(u'lex_lexicalform')

        # Adding field 'Representation.form'
        db.add_column(u'lex_representation', 'form',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='representations', to=orm['lex.Form']),
                      keep_default=False)

        # Deleting field 'Representation.lexical_form'
        db.delete_column(u'lex_representation', 'lexical_form_id')

        # Adding unique constraint on 'Representation', fields ['form', 'representation_type']
        db.create_unique(u'lex_representation', ['form_id', 'representation_type_id'])

        # Adding field 'Form.is_lemma'
        db.add_column(u'lex_form', 'is_lemma',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Form.lexeme'
        db.add_column(u'lex_form', 'lexeme',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='forms', to=orm['lex.Lexeme']),
                      keep_default=False)


    models = {
        u'lex.collection': {
            'Meta': {'object_name': 'Collection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexemes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collections'", 'symmetrical': 'False', 'to': u"orm['lex.Lexeme']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'lex.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.featurevalue': {
            'Meta': {'unique_together': "(('name', 'feature'),)", 'object_name': 'FeatureValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['lex.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.form': {
            'Meta': {'object_name': 'Form'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forms'", 'symmetrical': 'False', 'to': u"orm['lex.FeatureValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexemes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forms'", 'symmetrical': 'False', 'through': u"orm['lex.LexicalForm']", 'to': u"orm['lex.Lexeme']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.language': {
            'Meta': {'ordering': "('lang_code',)", 'unique_together': "(('lang_code', 'region_code'),)", 'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'})
        },
        u'lex.lexeme': {
            'Meta': {'object_name': 'Lexeme'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexemes'", 'to': u"orm['term.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lex_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexemes'", 'to': u"orm['lex.LexicalClass']"}),
            'lex_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'lex.lexicalclass': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'LexicalClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_classes'", 'to': u"orm['lex.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.lexicalform': {
            'Meta': {'object_name': 'LexicalForm'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_forms'", 'to': u"orm['lex.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_lemma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_forms'", 'to': u"orm['lex.Lexeme']"})
        },
        u'lex.representation': {
            'Meta': {'unique_together': "(('lexical_form', 'representation_type'),)", 'object_name': 'Representation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexical_form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representations'", 'to': u"orm['lex.LexicalForm']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representation_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representations'", 'to': u"orm['lex.RepresentationType']"})
        },
        u'lex.representationtype': {
            'Meta': {'object_name': 'RepresentationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'term.concept': {
            'Meta': {'object_name': 'Concept'},
            'concept_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'concepts'", 'symmetrical': 'False', 'to': u"orm['term.SubjectField']"})
        },
        u'term.subjectfield': {
            'Meta': {'object_name': 'SubjectField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['lex']