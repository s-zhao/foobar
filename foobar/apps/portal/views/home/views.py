# Create your views here. 
import os, json

from django.http import HttpResponse
from django.shortcuts import render_to_response 

#
# need RequestContext to push user ... etc to template
#
# https://docs.djangoproject.com/en/1.2/ref/templates/api/#subclassing-context-requestcontext
#
from django.template import RequestContext

from django.conf import settings

def foobar(request, *args, **kwargs):
    return render_to_response('foobar.html', {}, RequestContext(request) )
    
def index(request, *args, **kwargs):
    print request.META['REMOTE_ADDR']
    return render_to_response('portal/home/index.html', {}, RequestContext(request) )
    
def load_tpl(request, **kwargs):
    tpl = kwargs.get('tpl', 'story')
    if tpl == 'story':
        tpl = ["portal/partials/%s.html" % t for t in ['hot-story', 'story']]
    else:
        tpl = "portal/partials/%s.html" % tpl
        
    context = {'whoami': 'joe', 'templates': tpl}
    return render_to_response(tpl, context) #tpl: template or templates

def get_src(request, **kwargs):
    which = kwargs.get('scriptfile', 'views')
    
    srcfile = os.path.join(settings.Z_PROJECT_ROOT, 'foobar', 'apps', 'portal', 'views', 'home', '%s.py' % which)
    src = open(srcfile, 'rb').read()
    return HttpResponse(src, content_type="text/plain")
    
def get_json(request):
    d = []
    d.append({'name': 'joe', 'score': 50})
    d.append({'name': 'dave', 'score': 150})
    d.append({'name': 'john', 'score': 60})
    d.append({'name': 'phil', 'score': 80})
    d.append({'name': 'martin', 'score': 101})
    
    data = json.dumps(d)    
    return HttpResponse(data, content_type="application/json")
    
def get_errors(request):
    d = [{'key': 'invalid', 'message': 'invalid data'}, 
         {'key': 'required', 'message': 'field is required'}]
    
    data = json.dumps(d)
    return HttpResponse(data, content_type="application/json")
    

def books(request):
    d = []
    d.append({'title': 'angular JS', 'author': 'Brad Green and Shyam Seshadri'})
    d.append({'title': 'angular JS', 'author': 'Brad Green and Shyam Seshadri'})

    data = json.dumps(d)    
    return HttpResponse(data, content_type="application/json")
    
def books_book(request, slug):
    d = {'title': 'angular JS', 'author': 'Brad Green and Shyam Seshadri', 
         'description': 'This book introduces the quantum theory of angular momentum ...'}
    data = json.dumps(d)    
    return HttpResponse(data, content_type="application/json")         
    
def ng_template_books(request):
    return render_to_response('portal/partials/ng-templates/books.html')
    
def ng_template_books_book(request):
    return render_to_response('portal/partials/ng-templates/book.html')    
        