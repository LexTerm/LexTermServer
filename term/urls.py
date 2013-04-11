from django.conf.urls import patterns, url

urlpatterns = patterns('term.views',
    url(r'^subjects/$', 'list_subjects'),
    url(r'^concepts/$', 'list_concepts'),
    url(r'^concepts/(?P<id>\d+)/$', 'get_concept'),
    url(r'^lemmas/(?P<lemma>\w+)/$', 'search_concept'),
    url(r'^subjects/(?P<subject>\w+)/concepts/$', 'list_concepts'),
    url(r'^subjects/(?P<subject>\w+)/concepts/(?P<id>\d+)/$', 'get_concept'),
    url(r'^subjects/(?P<subject>\w+)/lemmas/(?P<lemma>\w+)/$', 'search_concept')
)

