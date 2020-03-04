from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.utils.translation import ugettext_lazy as _
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view


def bad(request):
    """
    Trigger error
    :return:
    """
    return 1/0
schema_view = get_swagger_view(title='Django Sample Project API')


urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("jet/", include("jet.urls", namespace='jet')),  # Django JET URLS
    path("jet/dashboard/", include('jet.dashboard.urls', namespace='jet-dashboard')),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # path("users/", include("apps.users.urls", namespace="users")),

    # path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    path('api/v1/', include('apps.services.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('bad', bad)
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = _('Django Sample Project')

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('docs/', schema_view),
        ]

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
