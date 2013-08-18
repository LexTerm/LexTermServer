from django.conf.urls import patterns, url
from lex import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', views.LanguageList.as_view()),
    # url(r'^(?P<lang>[a-z]{3})/$', '')
    url(r'^(?P<lang>[a-z]{3})/enums/$', views.EnumView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/enums/(?P<enum_name>\w+)/$', views.EnumView.as_view()),
    url(r'^(?P<lang>[a-z]{3})/representations/$', views.RepTypeList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/$', views.LexicalClassList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/(?P<class_name>\w+)/$', views.LexicalClassList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/$', views.LexemeList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/(?P<id>\d+)/$', views.Lexeme.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lemmas/(?P<lemma>\d+)/$', views.LexemeList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
