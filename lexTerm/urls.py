from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from lex.views import LanguageView, LexicalClassView, LexemeView, \
    FormView, FeatureValueView, FeatureView, RepresentationView, \
    RepresentationTypeView, CollectionView
from term.views import ConceptView, SubjectFieldView, NoteView


class LexTermApiRouter(DefaultRouter):

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(APIView):
            """
            TODO: Describe the api.
            """

            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {'tbx': reverse('tbx', request=request, format=format)}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(
                        url_name,
                        request=request,
                        format=format)
                return Response(ret)

        return APIRoot.as_view()


router = LexTermApiRouter()
router.register('languages', LanguageView)
router.register('lexicalclasses', LexicalClassView)
router.register('lexemes', LexemeView)
router.register('forms', FormView)
router.register('featurevalues', FeatureValueView)
router.register('features', FeatureView)
router.register('representations', RepresentationView)
router.register('representationtypes', RepresentationTypeView)
router.register('concepts', ConceptView)
router.register('subjectfields', SubjectFieldView)
router.register('notes', NoteView)
router.register('collections', CollectionView)

admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^$', 'lexTerm.views.home', name='home'),
    url(r'^api/', include(router.urls), name="api"),
    url(r'^api/tbx/', include('tbx.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^favicon\.ico$', RedirectView.as_view(url='static/favicon.ico'))
    )
