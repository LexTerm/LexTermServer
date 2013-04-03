from django.conf.urls import patterns, url

urlpatterns = patterns('term.views',
    url(r'^concept/$', 'list_concepts'),
    url(r'^concept/(?P<id>\d+)/$', 'get_concept'),
    url(r'^search/(?P<lemma>\w+)/$', 'search_concept')
)

