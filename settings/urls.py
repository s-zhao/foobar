from django.conf.urls import patterns, include, url


#from tastypie.api import Api
#from foobar.apps.portal.restful import MakerResource

#v1_api = Api(api_name='v1')
#v1_api.register(MakerResource())

"""
urlpatterns = patterns('',
    # The normal jazz here...
    (r'^blog/', include('myapp.urls')),
    (r'^api/', include(v1_api.urls)),
)
"""


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foobar.views.home', name='home'),
    # url(r'^foobar/', include('foobar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    #
    # django auth http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/
    # http://peyman-django.blogspot.com/2010/03/full-easy-authentication-using.html
    ('^user/', include('django.contrib.auth.urls')),
    
    #
    # include takes the form - r'^', r'^path/', r'^path/path/', ..., without ending $
    #
    url(r'^', include('foobar.apps.portal.urls')),
    #url(r'^api/', include(v1_api.urls)),
)
