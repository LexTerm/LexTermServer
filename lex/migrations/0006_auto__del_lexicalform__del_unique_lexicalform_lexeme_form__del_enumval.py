# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RepresentationType', fields ['name', 'language']
        db.delete_unique(u'lex_representationtype', ['name', 'language_id'])

        # Removing unique constraint on 'Form', fields ['name', 'lexicalClass']
        db.delete_unique(u'lex_form', ['name', 'lexicalClass_id'])

        # Removing unique constraint on 'Enumeration', fields ['name', 'language']
        db.delete_unique(u'lex_enumeration', ['name', 'language_id'])

        # Removing unique constraint on 'EnumValue', fields ['value', 'enum']
        db.delete_unique(u'lex_enumvalue', ['value', 'enum_id'])

        # Removing unique constraint on 'LexicalForm', fields ['lexeme', 'form']
        db.delete_unique(u'lex_lexicalform', ['lexeme_id', 'form_id'])

        # Deleting model 'LexicalForm'
        db.delete_table(u'lex_lexicalform')

        # Deleting model 'EnumValue'
        db.delete_table(u'lex_enumvalue')

        # Deleting model 'FeatureSet'
        db.delete_table(u'lex_featureset')

        # Deleting model 'FormValue'
        db.delete_table(u'lex_formvalue')

        # Deleting model 'Enumeration'
        db.delete_table(u'lex_enumeration')

        # Adding model 'FeatureValue'
        db.create_table(u'lex_featurevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Feature'])),
        ))
        db.send_create_signal(u'lex', ['FeatureValue'])

        # Adding unique constraint on 'FeatureValue', fields ['value', 'feature']
        db.create_unique(u'lex_featurevalue', ['value', 'feature_id'])

        # Deleting field 'Representation.representationType'
        db.delete_column(u'lex_representation', 'representationType_id')

        # Deleting field 'Representation.lexical_form'
        db.delete_column(u'lex_representation', 'lexical_form_id')

        # Adding field 'Representation.form'
        db.add_column(u'lex_representation', 'form',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='representations', to=orm['lex.Form']),
                      keep_default=False)

        # Adding field 'Representation.representation_type'
        db.add_column(u'lex_representation', 'representation_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='representations', to=orm['lex.RepresentationType']),
                      keep_default=False)

        # Deleting field 'Lexeme.language'
        db.delete_column(u'lex_lexeme', 'language_id')

        # Deleting field 'Lexeme.lexicalClass'
        db.delete_column(u'lex_lexeme', 'lexicalClass_id')

        # Adding field 'Lexeme.lex_class'
        db.add_column(u'lex_lexeme', 'lex_class',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='lexemes', to=orm['lex.LexicalClass']),
                      keep_default=False)

        # Deleting field 'Form.lexicalClass'
        db.delete_column(u'lex_form', 'lexicalClass_id')

        # Adding field 'Form.lexeme'
        db.add_column(u'lex_form', 'lexeme',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='forms', to=orm['lex.Lexeme']),
                      keep_default=False)

        # Adding M2M table for field features on 'Form'
        m2m_table_name = db.shorten_name(u'lex_form_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('form', models.ForeignKey(orm[u'lex.form'], null=False)),
            ('featurevalue', models.ForeignKey(orm[u'lex.featurevalue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['form_id', 'featurevalue_id'])

        # Deleting field 'RepresentationType.language'
        db.delete_column(u'lex_representationtype', 'language_id')

        # Deleting field 'Feature.lexicalClass'
        db.delete_column(u'lex_feature', 'lexicalClass_id')

        # Deleting field 'Feature.values'
        db.delete_column(u'lex_feature', 'values_id')


    def backwards(self, orm):
        # Removing unique constraint on 'FeatureValue', fields ['value', 'feature']
        db.delete_unique(u'lex_featurevalue', ['value', 'feature_id'])

        # Adding model 'LexicalForm'
        db.create_table(u'lex_lexicalform', (
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['lex.Lexeme'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Form'])),
        ))
        db.send_create_signal(u'lex', ['LexicalForm'])

        # Adding unique constraint on 'LexicalForm', fields ['lexeme', 'form']
        db.create_unique(u'lex_lexicalform', ['lexeme_id', 'form_id'])

        # Adding model 'EnumValue'
        db.create_table(u'lex_enumvalue', (
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Enumeration'])),
        ))
        db.send_create_signal(u'lex', ['EnumValue'])

        # Adding unique constraint on 'EnumValue', fields ['value', 'enum']
        db.create_unique(u'lex_enumvalue', ['value', 'enum_id'])

        # Adding model 'FeatureSet'
        db.create_table(u'lex_featureset', (
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Lexeme'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.EnumValue'])),
        ))
        db.send_create_signal(u'lex', ['FeatureSet'])

        # Adding model 'FormValue'
        db.create_table(u'lex_formvalue', (
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.EnumValue'])),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Feature'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['lex.Form'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'lex', ['FormValue'])

        # Adding model 'Enumeration'
        db.create_table(u'lex_enumeration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'lex', ['Enumeration'])

        # Adding unique constraint on 'Enumeration', fields ['name', 'language']
        db.create_unique(u'lex_enumeration', ['name', 'language_id'])

        # Deleting model 'FeatureValue'
        db.delete_table(u'lex_featurevalue')


        # User chose to not deal with backwards NULL issues for 'Representation.representationType'
        raise RuntimeError("Cannot reverse this migration. 'Representation.representationType' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Representation.representationType'
        db.add_column(u'lex_representation', 'representationType',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.RepresentationType']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Representation.lexical_form'
        raise RuntimeError("Cannot reverse this migration. 'Representation.lexical_form' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Representation.lexical_form'
        db.add_column(u'lex_representation', 'lexical_form',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='representations', to=orm['lex.LexicalForm']),
                      keep_default=False)

        # Deleting field 'Representation.form'
        db.delete_column(u'lex_representation', 'form_id')

        # Deleting field 'Representation.representation_type'
        db.delete_column(u'lex_representation', 'representation_type_id')


        # User chose to not deal with backwards NULL issues for 'Lexeme.language'
        raise RuntimeError("Cannot reverse this migration. 'Lexeme.language' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Lexeme.language'
        db.add_column(u'lex_lexeme', 'language',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Lexeme.lexicalClass'
        raise RuntimeError("Cannot reverse this migration. 'Lexeme.lexicalClass' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Lexeme.lexicalClass'
        db.add_column(u'lex_lexeme', 'lexicalClass',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.LexicalClass']),
                      keep_default=False)

        # Deleting field 'Lexeme.lex_class'
        db.delete_column(u'lex_lexeme', 'lex_class_id')


        # User chose to not deal with backwards NULL issues for 'Form.lexicalClass'
        raise RuntimeError("Cannot reverse this migration. 'Form.lexicalClass' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Form.lexicalClass'
        db.add_column(u'lex_form', 'lexicalClass',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['lex.LexicalClass']),
                      keep_default=False)

        # Deleting field 'Form.lexeme'
        db.delete_column(u'lex_form', 'lexeme_id')

        # Removing M2M table for field features on 'Form'
        db.delete_table(db.shorten_name(u'lex_form_features'))

        # Adding unique constraint on 'Form', fields ['name', 'lexicalClass']
        db.create_unique(u'lex_form', ['name', 'lexicalClass_id'])


        # User chose to not deal with backwards NULL issues for 'RepresentationType.language'
        raise RuntimeError("Cannot reverse this migration. 'RepresentationType.language' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'RepresentationType.language'
        db.add_column(u'lex_representationtype', 'language',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Language']),
                      keep_default=False)

        # Adding unique constraint on 'RepresentationType', fields ['name', 'language']
        db.create_unique(u'lex_representationtype', ['name', 'language_id'])


        # User chose to not deal with backwards NULL issues for 'Feature.lexicalClass'
        raise RuntimeError("Cannot reverse this migration. 'Feature.lexicalClass' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Feature.lexicalClass'
        db.add_column(u'lex_feature', 'lexicalClass',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='features', to=orm['lex.LexicalClass']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Feature.values'
        raise RuntimeError("Cannot reverse this migration. 'Feature.values' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Feature.values'
        db.add_column(u'lex_feature', 'values',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lex.Enumeration']),
                      keep_default=False)


    models = {
        u'lex.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.featurevalue': {
            'Meta': {'unique_together': "(('value', 'feature'),)", 'object_name': 'FeatureValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['lex.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lex.form': {
            'Meta': {'ordering': "('preference',)", 'object_name': 'Form'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forms'", 'symmetrical': 'False', 'to': u"orm['lex.FeatureValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forms'", 'to': u"orm['lex.Lexeme']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'preference': ('django.db.models.fields.IntegerField', [], {})
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
            'subjectFields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['term.SubjectField']", 'symmetrical': 'False'})
        },
        u'term.subjectfield': {
            'Meta': {'object_name': 'SubjectField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['lex']