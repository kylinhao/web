from django.conf.urls import include, url
from django.contrib import admin



urlpatterns = [
    # Examples:
    # url(r'^$', 'JXXT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'ustcjxxt.views.login'),
    url(r'^assistant/', 'ustcjxxt.views.assistant'),
    url(r"^logout/",'ustcjxxt.views.logout'),
]

# urlpatterns +=[
#     url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),
#     url( r'^templates/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.TEMPLATE_DIRS }),
# ]