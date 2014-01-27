# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RepresentationType', fields ['name', 'language']
        db.delete_unique(u'lex_representationtype', ['name', 'language_id'])

        # Deleting model 'RepresentationType'
        db.delete_table(u'lex_representationtype')

        # Deleting field 'Representation.representationType'
        db.delete_column(u'lex_representation', 'representationType_id')


    def backwards(self, orm):
        # Adding model 'RepresentationType'
        db.create_table(u'lex_representationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['RepresentationType'])

        # Adding unique constraint on 'RepresentationType', fields ['name', 'language']
        db.create_unique(u'lex_representationtype', ['name', 'language_id'])


        # User chose to not deal with backwards NULL issues for 'Representation.representationType'
        raise RuntimeError("Cannot reverse this migration. 'Representation.representationType' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Representation.representationType'
        db.add_column(u'lex_representation', 'representationType',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.RepresentationType']),
                      keep_default=False)


    models = {
        u'lex.enumeration': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'Enumeration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.enumvalue': {
            'Meta': {'unique_together': "(('value', 'enum'),)", 'object_name': 'EnumValue'},
            'enum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['lex.Enumeration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexicalClass': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'features'", 'to': u"orm['lex.LexicalClass']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'values': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Enumeration']"})
        },
        u'lex.featureset': {
            'Meta': {'object_name': 'FeatureSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Lexeme']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.EnumValue']"})
        },
        u'lex.form': {
            'Meta': {'ordering': "('preference',)", 'unique_together': "(('name', 'lexicalClass'),)", 'object_name': 'Form'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexicalClass': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forms'", 'to': u"orm['lex.LexicalClass']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'preference': ('django.db.models.fields.IntegerField', [], {})
        },
        u'lex.formvalue': {
            'Meta': {'object_name': 'FormValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Feature']"}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['lex.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.EnumValue']"})
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
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'terms'", 'null': 'True', 'to': u"orm['term.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Language']"}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lex_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'lexicalClass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.LexicalClass']"})
        },
        u'lex.lexicalclass': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'LexicalClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.lexicalform': {
            'Meta': {'unique_together': "(('lexeme', 'form'),)", 'object_name': 'LexicalForm'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forms'", 'to': u"orm['lex.Lexeme']"}),
            'representation': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'lex.representation': {
            'Meta': {'object_name': 'Representation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Lexeme']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.termnote': {
            'Meta': {'object_name': 'TermNote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'term_notes'", 'to': u"orm['lex.Lexeme']"}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'note_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'term.concept': {
            'Meta': {'object_name': 'Concept'},
            'concept_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subjectFields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['term.SubjectField']", 'symmetrical': 'False'})
        },
        u'term.subjectfield': {
            'Meta': {'object_name': 'SubjectField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['lex']