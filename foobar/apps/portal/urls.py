from django.conf.urls import patterns, include, url

urlpatterns = patterns('',    
    url(r'^', include('foobar.apps.portal.views.home.urls')),

)
