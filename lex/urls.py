from django.conf.urls import patterns, url
from lex import views

urlpatterns = patterns('',
    url(r'^/$', views.LangList.as_view()),
    # url(r'^(?P<lang>[a-z]{3})/$', '')
    url(r'^(?P<lang>[a-z]{3})/enums/$', views.EnumList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/enums/(?P<enum_name>\w+)/$', views.Enum.as_view()),
    url(r'^(?P<lang>[a-z]{3})/representations/$', views.RepList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/$', views.LexClassList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/classes/(?P<class_name>\w+)/$', views.LexClass.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/$', views.LexemeList.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lexemes/(?P<id>\d+)/$', views.Lexeme.as_view()),
    url(r'^(?P<lang>[a-z]{3})/lemmas/(?P<lemma>\d+)/$', views.LexemeList.as_view()),
)

