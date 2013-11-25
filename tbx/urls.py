from django.conf.urls import patterns, url
from tbx.views import *

urlpatterns = patterns('',
    url(r'^$', tbx_root),
    url(r'^import/$', TBXImportView.as_view(), name='tbx_import'),
    url(r'^export/$', TBXExportView.as_view(), name='tbx_export')
)

