# coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect,HttpResponse
from .models import Student
# from django.http import Http404
# from django.template import RequestContext
# from django.views.decorators.csrf import csrf_exempt
username = ""

# @csrf_exempt
def login(req):
    if req.method == 'POST':
        userId = req.POST.get("userId", "")
        pwd = req.POST.get("password", "")
        typeValue = req.POST.get("radio", "")
        print typeValue
        user = Student.objects.filter(stuId=userId, password=pwd)
        if user:
            req.session['username'] = user[0].name;
            return HttpResponseRedirect('/assistant/')
        else:
            return HttpResponseNotFound('<h1>用户名密码错误</h1>')
    else:
        return render_to_response('login.html', {})


def assistant(req):
    username = req.session.get('username','null')
    if username != 'null':
        return render_to_response('assistant.html',{"username":username})
    else:
        return HttpResponseRedirect('/login/')


def logout(req):
    try:
        del req.session['username']
        return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/login/')
