# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'FeatureValue', fields ['value', 'feature']
        db.delete_unique(u'lex_featurevalue', ['value', 'feature_id'])

        # Deleting field 'Form.preference'
        db.delete_column(u'lex_form', 'preference')

        # Adding field 'Form.is_lemma'
        db.add_column(u'lex_form', 'is_lemma',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'FeatureValue.value'
        db.delete_column(u'lex_featurevalue', 'value')

        # Adding field 'FeatureValue.name'
        db.add_column(u'lex_featurevalue', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding unique constraint on 'FeatureValue', fields ['name', 'feature']
        db.create_unique(u'lex_featurevalue', ['name', 'feature_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeatureValue', fields ['name', 'feature']
        db.delete_unique(u'lex_featurevalue', ['name', 'feature_id'])


        # User chose to not deal with backwards NULL issues for 'Form.preference'
        raise RuntimeError("Cannot reverse this migration. 'Form.preference' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Form.preference'
        db.add_column(u'lex_form', 'preference',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Deleting field 'Form.is_lemma'
        db.delete_column(u'lex_form', 'is_lemma')


        # User chose to not deal with backwards NULL issues for 'FeatureValue.value'
        raise RuntimeError("Cannot reverse this migration. 'FeatureValue.value' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'FeatureValue.value'
        db.add_column(u'lex_featurevalue', 'value',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)

        # Deleting field 'FeatureValue.name'
        db.delete_column(u'lex_featurevalue', 'name')

        # Adding unique constraint on 'FeatureValue', fields ['value', 'feature']
        db.create_unique(u'lex_featurevalue', ['value', 'feature_id'])


    models = {
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
            'is_lemma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forms'", 'to': u"orm['lex.Lexeme']"}),
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
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lexemes'", 'null': 'True', 'to': u"orm['term.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lex_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexemes'", 'to': u"orm['lex.LexicalClass']"}),
            'lex_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'lex.lexicalclass': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'LexicalClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_classes'", 'to': u"orm['lex.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.representation': {
            'Meta': {'object_name': 'Representation'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representations'", 'to': u"orm['lex.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representation_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representations'", 'to': u"orm['lex.RepresentationType']"})
        },
        u'lex.representationtype': {
            'Meta': {'object_name': 'RepresentationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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