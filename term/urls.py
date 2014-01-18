from django.conf.urls import patterns, include, url
from term.views import *

list_actions = {'get': 'list', 'post': 'create'}
detail_actions = {'get': 'retrieve', 'put': 'create', 'delete': 'destroy'}

urlpatterns = patterns(
    '',
    url(r'^$', term_root, name="term"),
    url(r'^tbx/', include('tbx.urls')),
    url(r'^subjects/$', SubjectView.as_view(list_actions), name='subject_view'),
    url(r'^subjects/(?P<name>\w+)/$', SubjectView.as_view(detail_actions), name='subject_detail'),
    url(r'^concepts/$', ConceptView.as_view(list_actions), name='concept_view'),
    url(r'^concepts/(?P<id>\d+)/$', ConceptView.as_view(detail_actions)),
    url(r'^subjects/(?P<subject>\w+)/concepts/$', ConceptView.as_view(list_actions)),
    url(r'^subjects/(?P<subject>\w+)/concepts/(?P<id>\d+)/$', ConceptView.as_view(detail_actions)),
    # url(r'^lemmas/(?P<lemma>\w+)/$', Lemma.as_view()),
    # url(r'^subjects/(?P<subject>\w+)/lemmas/(?P<lemma>\w+)/$', Lemma.as_view()),
)
