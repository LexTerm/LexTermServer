from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lexTerm.views.home', name='home'),
    # url(r'^lexTerm/', include('lexTerm.foo.urls')),
    url(r'^api/lex/', include('lex.urls')),
    url(r'^api/term/', include('term.urls')),
    url(r'^api/tbx/', include('tbx.urls')),
    url(r'^admin/', include(admin.site.urls)),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
