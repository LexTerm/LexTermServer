# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'lex_language', (
            ('langCode', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Language'])

        # Adding model 'LexicalClass'
        db.create_table(u'lex_lexicalclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
        ))
        db.send_create_signal(u'lex', ['LexicalClass'])

        # Adding unique constraint on 'LexicalClass', fields ['name', 'language']
        db.create_unique(u'lex_lexicalclass', ['name', 'language_id'])

        # Adding model 'Form'
        db.create_table(u'lex_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lexicalClass', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['lex.LexicalClass'])),
            ('preference', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'lex', ['Form'])

        # Adding unique constraint on 'Form', fields ['name', 'lexicalClass']
        db.create_unique(u'lex_form', ['name', 'lexicalClass_id'])

        # Adding model 'Enumeration'
        db.create_table(u'lex_enumeration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
        ))
        db.send_create_signal(u'lex', ['Enumeration'])

        # Adding unique constraint on 'Enumeration', fields ['name', 'language']
        db.create_unique(u'lex_enumeration', ['name', 'language_id'])

        # Adding model 'EnumValue'
        db.create_table(u'lex_enumvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('enum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Enumeration'])),
        ))
        db.send_create_signal(u'lex', ['EnumValue'])

        # Adding unique constraint on 'EnumValue', fields ['value', 'enum']
        db.create_unique(u'lex_enumvalue', ['value', 'enum_id'])

        # Adding model 'Feature'
        db.create_table(u'lex_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lexicalClass', self.gf('django.db.models.fields.related.ForeignKey')(related_name='features', to=orm['lex.LexicalClass'])),
            ('values', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Enumeration'])),
        ))
        db.send_create_signal(u'lex', ['Feature'])

        # Adding model 'FormValue'
        db.create_table(u'lex_formvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Form'])),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Feature'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.EnumValue'])),
        ))
        db.send_create_signal(u'lex', ['FormValue'])

        # Adding model 'Lexeme'
        db.create_table(u'lex_lexeme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lex_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
            ('lexicalClass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.LexicalClass'])),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='terms', null=True, to=orm['term.Concept'])),
            ('lemma', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'lex', ['Lexeme'])

        # Adding model 'TermNote'
        db.create_table(u'lex_termnote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='term_notes', to=orm['lex.Lexeme'])),
            ('note_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'lex', ['TermNote'])

        # Adding model 'LexicalForm'
        db.create_table(u'lex_lexicalform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['lex.Lexeme'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Form'])),
            ('representation', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'lex', ['LexicalForm'])

        # Adding unique constraint on 'LexicalForm', fields ['lexeme', 'form']
        db.create_unique(u'lex_lexicalform', ['lexeme_id', 'form_id'])

        # Adding model 'RepresentationType'
        db.create_table(u'lex_representationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
        ))
        db.send_create_signal(u'lex', ['RepresentationType'])

        # Adding unique constraint on 'RepresentationType', fields ['name', 'language']
        db.create_unique(u'lex_representationtype', ['name', 'language_id'])

        # Adding model 'Representation'
        db.create_table(u'lex_representation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Lexeme'])),
            ('representationType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.RepresentationType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Representation'])

        # Adding model 'FeatureSet'
        db.create_table(u'lex_featureset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Lexeme'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.EnumValue'])),
        ))
        db.send_create_signal(u'lex', ['FeatureSet'])


    def backwards(self, orm):
        # Removing unique constraint on 'RepresentationType', fields ['name', 'language']
        db.delete_unique(u'lex_representationtype', ['name', 'language_id'])

        # Removing unique constraint on 'LexicalForm', fields ['lexeme', 'form']
        db.delete_unique(u'lex_lexicalform', ['lexeme_id', 'form_id'])

        # Removing unique constraint on 'EnumValue', fields ['value', 'enum']
        db.delete_unique(u'lex_enumvalue', ['value', 'enum_id'])

        # Removing unique constraint on 'Enumeration', fields ['name', 'language']
        db.delete_unique(u'lex_enumeration', ['name', 'language_id'])

        # Removing unique constraint on 'Form', fields ['name', 'lexicalClass']
        db.delete_unique(u'lex_form', ['name', 'lexicalClass_id'])

        # Removing unique constraint on 'LexicalClass', fields ['name', 'language']
        db.delete_unique(u'lex_lexicalclass', ['name', 'language_id'])

        # Deleting model 'Language'
        db.delete_table(u'lex_language')

        # Deleting model 'LexicalClass'
        db.delete_table(u'lex_lexicalclass')

        # Deleting model 'Form'
        db.delete_table(u'lex_form')

        # Deleting model 'Enumeration'
        db.delete_table(u'lex_enumeration')

        # Deleting model 'EnumValue'
        db.delete_table(u'lex_enumvalue')

        # Deleting model 'Feature'
        db.delete_table(u'lex_feature')

        # Deleting model 'FormValue'
        db.delete_table(u'lex_formvalue')

        # Deleting model 'Lexeme'
        db.delete_table(u'lex_lexeme')

        # Deleting model 'TermNote'
        db.delete_table(u'lex_termnote')

        # Deleting model 'LexicalForm'
        db.delete_table(u'lex_lexicalform')

        # Deleting model 'RepresentationType'
        db.delete_table(u'lex_representationtype')

        # Deleting model 'Representation'
        db.delete_table(u'lex_representation')

        # Deleting model 'FeatureSet'
        db.delete_table(u'lex_featureset')


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
            'Meta': {'ordering': "('langCode',)", 'object_name': 'Language'},
            'langCode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representationType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.RepresentationType']"})
        },
        u'lex.representationtype': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'RepresentationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lex.Language']"}),
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