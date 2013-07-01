from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testExi.views.home', name='home'),
    # url(r'^testExi/', include('testExi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', include('geo.urls')),
    (r'^index/$', include('geo.urls')),
    (r'^register/$', include('geo.urls')),
    (r'^logout/$', 'geo.views.LogoutRequest'),
    (r'^login/$', 'geo.views.LoginRequest'),
    (r'^json_get_latest_waypoint','geo.views.json_get_latest_waypoint'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
