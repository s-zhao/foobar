from django.conf.urls import patterns, include, url

urlpatterns = patterns('foobar.apps.portal.views.home.views',    
    url(r'^$', 'index', name='portal-index'), 
    url(r'^load-tpl/(?P<tpl>\w+)/$', 'load_tpl', name='portal-load-template'),
    url(r'^get-src/(?P<scriptfile>\w+)/$', 'get_src', name='portal-get-src'),
    url(r'^get-json/$', 'get_json', name='portal-get-json'),
    url(r'^get-errors/$', 'get_errors', name='portal-get-errors'),
    url(r'^books/$', 'books', name='portal-books'),
    url(r'^ng-template/books/$', 'ng_template_books', name='portal-ng-template-books'),
    url(r'^books/(?P<slug>[a-zA-Z0-9\-]+)/$', 'books_book', name='portal-books-book'),
    url(r'^ng-template/books/book/$', 'ng_template_books_book', name='portal-ng-template-books-book'),
    
)
