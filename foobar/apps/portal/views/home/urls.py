from django.conf.urls import patterns, include, url

#
# url naming: {app-label}-{path/to/view}-{path/to/function}
# 
urlpatterns = patterns('foobar.apps.portal.views.home.views',    
    url(r'^$', 'index', name='portal-home-index'), 
    
    url(r'^snippets/angular/$', 'snippets_angular', name='portal-home-snippets-angular'),
    url(r'^snippets/angular/(?P<snippet>[\-\.\w]+)/$', 'snippets_angular', name='portal-home-snippets-angular-snippet'),

    url(r'^angular/page/$', 'get_angular_page', name='portal-home-get-angular-page'),
    url(r'^angular/page/(?P<page>[\-\.\w]+)/$', 'get_angular_page', name='portal-home-get-angular-page-page'),

    url(r'^snippets/django/$', 'snippets_django', name='portal-home-snippets-django'),
    url(r'^snippets/django/(?P<snippet>[\-\.\w]+)/$', 'snippets_django', name='portal-home-snippets-django-snippet'),
    
    
    
    
    url(r'^snippets/*', 'snippets', name='portal-home-snippets'),
    url(r'^load-tpl/(?P<tpl>\w+)/$', 'load_tpl', name='portal-home-load-template'),
    url(r'^get-src/(?P<scriptfile>\w+)/$', 'get_src', name='portal-home-get-src'),
    url(r'^get-json/$', 'get_json', name='portal-home-get-json'),
    url(r'^get-errors/$', 'get_errors', name='portal-home-get-errors'),
    url(r'^books/$', 'books', name='portal-home-books'),
    url(r'^ng-template/books/$', 'ng_template_books', name='portal-home-ng-template-books'),
    url(r'^books/(?P<slug>[a-zA-Z0-9\-]+)/$', 'books_book', name='portal-home-books-book'),
    url(r'^ng-template/books/book/$', 'ng_template_books_book', name='portal-home-ng-template-books-book'),
)
