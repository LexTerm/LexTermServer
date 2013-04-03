from django.conf.urls import patterns, url

urlpatterns = patterns('config.views',
    url(r'^langs/$', 'list_langs'),
    url(r'^subjects/$', 'list_subjects'),
    url(r'^(?P<lang>[a-z]{3})/enum/$', 'list_enums'),
    url(r'^(?P<lang>[a-z]{3})/enum/(?P<enum_name>\w+)/$', 'get_enum'),
    url(r'^(?P<lang>[a-z]{3})/representations/$', 'list_reps'),
    url(r'^(?P<lang>[a-z]{3})/classes/$', 'list_classes'),
    url(r'^(?P<lang>[a-z]{3})/classes/(?P<class_name>\w+)/$', 'get_class'),
)

