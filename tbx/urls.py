from django.conf.urls import patterns, url
from tbx.views import *

urlpatterns = patterns('',
    url(r'^$', ValidateView.as_view()),
)
