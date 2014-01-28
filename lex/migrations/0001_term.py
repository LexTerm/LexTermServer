# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'lex_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('region_code', self.gf('django.db.models.fields.CharField')(default='', max_length=3, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Language'])

        # Adding unique constraint on 'Language', fields ['lang_code', 'region_code']
        db.create_unique(u'lex_language', ['lang_code', 'region_code'])

        # Adding model 'LexicalClass'
        db.create_table(u'lex_lexicalclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexical_classes', to=orm['lex.Language'])),
        ))
        db.send_create_signal(u'lex', ['LexicalClass'])

        # Adding unique constraint on 'LexicalClass', fields ['name', 'language']
        db.create_unique(u'lex_lexicalclass', ['name', 'language_id'])

        # Adding model 'Lexeme'
        db.create_table(u'lex_lexeme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lex_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('lex_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexemes', to=orm['lex.LexicalClass'])),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexemes', to=orm['term.Concept'])),
        ))
        db.send_create_signal(u'lex', ['Lexeme'])

        # Adding model 'Feature'
        db.create_table(u'lex_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Feature'])

        # Adding model 'FeatureValue'
        db.create_table(u'lex_featurevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Feature'])),
        ))
        db.send_create_signal(u'lex', ['FeatureValue'])

        # Adding unique constraint on 'FeatureValue', fields ['name', 'feature']
        db.create_unique(u'lex_featurevalue', ['name', 'feature_id'])

        # Adding model 'Form'
        db.create_table(u'lex_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['lex.Lexeme'])),
            ('is_lemma', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'lex', ['Form'])

        # Adding M2M table for field features on 'Form'
        m2m_table_name = db.shorten_name(u'lex_form_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('form', models.ForeignKey(orm[u'lex.form'], null=False)),
            ('featurevalue', models.ForeignKey(orm[u'lex.featurevalue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['form_id', 'featurevalue_id'])

        # Adding model 'RepresentationType'
        db.create_table(u'lex_representationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'lex', ['RepresentationType'])

        # Adding model 'Representation'
        db.create_table(u'lex_representation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='representations', to=orm['lex.Form'])),
            ('representation_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='representations', to=orm['lex.RepresentationType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Representation'])

        # Adding unique constraint on 'Representation', fields ['form', 'representation_type']
        db.create_unique(u'lex_representation', ['form_id', 'representation_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Representation', fields ['form', 'representation_type']
        db.delete_unique(u'lex_representation', ['form_id', 'representation_type_id'])

        # Removing unique constraint on 'FeatureValue', fields ['name', 'feature']
        db.delete_unique(u'lex_featurevalue', ['name', 'feature_id'])

        # Removing unique constraint on 'LexicalClass', fields ['name', 'language']
        db.delete_unique(u'lex_lexicalclass', ['name', 'language_id'])

        # Removing unique constraint on 'Language', fields ['lang_code', 'region_code']
        db.delete_unique(u'lex_language', ['lang_code', 'region_code'])

        # Deleting model 'Language'
        db.delete_table(u'lex_language')

        # Deleting model 'LexicalClass'
        db.delete_table(u'lex_lexicalclass')

        # Deleting model 'Lexeme'
        db.delete_table(u'lex_lexeme')

        # Deleting model 'Feature'
        db.delete_table(u'lex_feature')

        # Deleting model 'FeatureValue'
        db.delete_table(u'lex_featurevalue')

        # Deleting model 'Form'
        db.delete_table(u'lex_form')

        # Removing M2M table for field features on 'Form'
        db.delete_table(db.shorten_name(u'lex_form_features'))

        # Deleting model 'RepresentationType'
        db.delete_table(u'lex_representationtype')

        # Deleting model 'Representation'
        db.delete_table(u'lex_representation')


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
        u'lex.representation': {
            'Meta': {'unique_together': "(('form', 'representation_type'),)", 'object_name': 'Representation'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representations'", 'to': u"orm['lex.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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