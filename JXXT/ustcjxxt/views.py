from django.shortcuts import render
from django.shortcuts import  render_to_response
from django.http import HttpResponse
# Create your views here.
#  t = get_template('login.html')
# html = t.render(Context({}))
# return HttpResponse(html)
# return render_to_response('login.html',{},context_instance=RequestContext(req))
def login(req):
    return render_to_response('login.html',{})

def index(req):
    return HttpResponse("OK")