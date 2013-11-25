from django.conf.urls import patterns, url
from lex.views import *
from rest_framework.urlpatterns import format_suffix_patterns

list_actions = {'get': 'list', 'post': 'create'}
detail_actions = {'get': 'retrieve', 'put': 'create', 'delete': 'destroy'}

urlpatterns = patterns('',
    # url(r'^(?P<langCode>[a-z]{3})/$', '')
    url(r'^$', lex_root),
    url(r'^lang/$', 
        LanguageView.as_view(list_actions), 
        name='language_list'),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/$', 
        LanguageView.as_view(detail_actions), 
        name='language_detail'),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/enums/$', 
        EnumView.as_view(list_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/enums/(?P<name>\w+)/$', 
        EnumView.as_view(detail_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/enums/(?P<name>\w+)/values/$', 
        EnumValueView.as_view(list_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/enums/(?P<name>\w+)/values/(?P<value>\w+)/$', 
        EnumValueView.as_view(detail_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/representations/$', 
        RepTypeView.as_view(list_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/representations/(?P<name>\w+)/$', 
        RepTypeView.as_view(detail_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/classes/$', 
        LexicalClassView.as_view(list_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/classes/(?P<name>\w+)/$', 
        LexicalClassView.as_view(detail_actions)),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/lexemes/$', 
        LexemeView.as_view(list_actions), 
        name='lexeme_list'),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/lexemes/(?P<id>[\w-]+)/$', 
        LexemeView.as_view(detail_actions), 
        name='lexeme_detail'),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/lexemes/(?P<id>[\w-]+)/forms/$', 
        LexicalFormView.as_view(list_actions),
        name='lexical_form_list'),
    url(r'^lang/(?P<langCode>[a-z]{2,3})/lexemes/(?P<id>[\w-]+)/forms/(?P<form>\w+)/$', 
        LexicalFormView.as_view(detail_actions),
        name='lexical_form_detail'),
    # url(r'^lang/(?P<langCode>[a-z]{2,3})/lemmas/(?P<lemma>\d+)/$', LexemeList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
