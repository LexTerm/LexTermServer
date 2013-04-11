from django.conf.urls import patterns, url

urlpatterns = patterns('lex.views',
    url(r'^/$', 'list_langs'),
    # url(r'^(?P<lang>[a-z]{3})/$', '')
    url(r'^(?P<lang>[a-z]{3})/enums/$', 'list_enums'),
    url(r'^(?P<lang>[a-z]{3})/enums/(?P<enum_name>\w+)/$', 'get_enum'),
    url(r'^(?P<lang>[a-z]{3})/representations/$', 'list_reps'),
    url(r'^(?P<lang>[a-z]{3})/classes/$', 'list_classes'),
    url(r'^(?P<lang>[a-z]{3})/classes/(?P<class_name>\w+)/$', 'get_class'),
    url(r'^(?P<lang>[a-z]{3})/lexemes/$', 'list_entries'),
    url(r'^(?P<lang>[a-z]{3})/lexemes/(?P<id>\d+)/$', 'get_entry'),
    # url(r'^(?P<lang>[a-z]{3})/lemmas/(?P<lemma>\d+)/$', 'search_entry'),
)

