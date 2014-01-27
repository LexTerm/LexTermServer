# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field subjectFields on 'Concept'
        db.delete_table(db.shorten_name(u'term_concept_subjectFields'))

        # Adding M2M table for field subject_fields on 'Concept'
        m2m_table_name = db.shorten_name(u'term_concept_subject_fields')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concept', models.ForeignKey(orm[u'term.concept'], null=False)),
            ('subjectfield', models.ForeignKey(orm[u'term.subjectfield'], null=False))
        ))
        db.create_unique(m2m_table_name, ['concept_id', 'subjectfield_id'])


    def backwards(self, orm):
        # Adding M2M table for field subjectFields on 'Concept'
        m2m_table_name = db.shorten_name(u'term_concept_subjectFields')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concept', models.ForeignKey(orm[u'term.concept'], null=False)),
            ('subjectfield', models.ForeignKey(orm[u'term.subjectfield'], null=False))
        ))
        db.create_unique(m2m_table_name, ['concept_id', 'subjectfield_id'])

        # Removing M2M table for field subject_fields on 'Concept'
        db.delete_table(db.shorten_name(u'term_concept_subject_fields'))


    models = {
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
            'lex_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexemes'", 'to': u"orm['lex.LexicalClass']"}),
            'lex_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'lex.lexicalclass': {
            'Meta': {'unique_together': "(('name', 'language'),)", 'object_name': 'LexicalClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_classes'", 'to': u"orm['lex.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'term.concept': {
            'Meta': {'object_name': 'Concept'},
            'concept_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'concepts'", 'symmetrical': 'False', 'to': u"orm['term.SubjectField']"})
        },
        u'term.note': {
            'Meta': {'object_name': 'Note'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': u"orm['lex.Lexeme']"}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'note_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'term.subjectfield': {
            'Meta': {'object_name': 'SubjectField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['term']