# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubjectField'
        db.create_table(u'term_subjectfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'term', ['SubjectField'])

        # Adding model 'Concept'
        db.create_table(u'term_concept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concept_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('definition', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'term', ['Concept'])

        # Adding M2M table for field subjectFields on 'Concept'
        m2m_table_name = db.shorten_name(u'term_concept_subjectFields')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('concept', models.ForeignKey(orm[u'term.concept'], null=False)),
            ('subjectfield', models.ForeignKey(orm[u'term.subjectfield'], null=False))
        ))
        db.create_unique(m2m_table_name, ['concept_id', 'subjectfield_id'])


    def backwards(self, orm):
        # Deleting model 'SubjectField'
        db.delete_table(u'term_subjectfield')

        # Deleting model 'Concept'
        db.delete_table(u'term_concept')

        # Removing M2M table for field subjectFields on 'Concept'
        db.delete_table(db.shorten_name(u'term_concept_subjectFields'))


    models = {
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

    complete_apps = ['term']