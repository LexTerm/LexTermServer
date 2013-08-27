from django.conf.urls import patterns, url
from lex.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', LanguageView.as_view()),
    # url(r'^(?P<lang>[a-z]{3})/$', '')
    url(r'^(?P<lang>[a-z]{3})/enums/$', EnumView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/enums/(?P<name>\w+)/$', EnumView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/representations/$', RepTypeView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/representations/(?P<name>\w+)/$', RepTypeView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/$', LexicalClassView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/(?P<name>\w+)/$', LexicalClassView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/$', LexemeView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/(?P<id>\d+)/$', LexemeView.as_view()),
    # url(r'^(?P<lang>[a-z]{3})/lemmas/(?P<lemma>\d+)/$', LexemeList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
