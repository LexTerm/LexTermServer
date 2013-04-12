from django.conf.urls import patterns, url
from term import views

urlpatterns = patterns('',
    url(r'^subjects/$', views.SubjectList.as_view()),
    url(r'^concepts/$', views.ConceptList.as_view()),
    url(r'^concepts/(?P<id>\d+)/$', views.Concept.as_view()),
    url(r'^lemmas/(?P<lemma>\w+)/$', views.Lemma.as_view()),
    url(r'^subjects/(?P<subject>\w+)/concepts/$', views.ConceptList.as_view()),
    url(r'^subjects/(?P<subject>\w+)/concepts/(?P<id>\d+)/$', views.Concept.as_view()),
    url(r'^subjects/(?P<subject>\w+)/lemmas/(?P<lemma>\w+)/$', views.Lemma.as_view()),
)

