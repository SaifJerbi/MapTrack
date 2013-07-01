# Import django modules
from django.conf.urls.defaults import *


urlpatterns = patterns('geo.views',
    url(r'^$', 'index', name='waypoints-index'),
    
    #url(r'^main/$', 'index'),
    (r'^login/$', 'LoginRequest'),
    #(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'geo/login.html'}),
    (r'^logout/$', 'LogoutRequest'),
    (r'^json_get_latest_waypoint/$', 'json_get_latest_waypoint'),
    
)