from django.conf.urls import patterns, url
from tbx.views import *

urlpatterns = patterns('',
    url(r'^$', tbx_root, name="tbx"),
    url(r'^validate/$', ValidateView.as_view(), name='tbx_validate'),
    url(r'^import/$', TBXImportView.as_view(), name='tbx_import'),
    url(r'^export/$', TBXExportView.as_view(), name='tbx_export')
)