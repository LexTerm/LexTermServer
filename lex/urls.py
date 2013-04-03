from django.conf.urls import patterns, url

urlpatterns = patterns('lex.views',
    # url(r'^(?P<lang>[a-z]{3})/$', ''),
    url(r'^(?P<lang>[a-z]{3})/$', 'list_entries'),
    url(r'^(?P<lang>[a-z]{3})/(?P<id>\d+)/$', 'get_entry'),
)

