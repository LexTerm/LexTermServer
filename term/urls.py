from django.conf.urls import patterns, url
from term.views import *

list_actions = {'get': 'list', 'post': 'create'}
detail_actions = {'get': 'retrieve', 'put': 'create', 'delete': 'destroy'}

urlpatterns = patterns('',
    url(r'^subjects/$', SubjectView.as_view()),
    url(r'^concepts/$', ConceptList.as_view()),
    url(r'^concepts/(?P<id>\d+)/$', Concept.as_view()),
    url(r'^lemmas/(?P<lemma>\w+)/$', Lemma.as_view()),
    url(r'^subjects/(?P<subject>\w+)/concepts/$', ConceptList.as_view()),
    url(r'^subjects/(?P<subject>\w+)/concepts/(?P<id>\d+)/$', Concept.as_view()),
    url(r'^subjects/(?P<subject>\w+)/lemmas/(?P<lemma>\w+)/$', Lemma.as_view()),
)

