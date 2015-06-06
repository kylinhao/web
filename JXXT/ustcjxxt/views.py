# coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from .models import Student, Teacher, Assistant
# from django.http import Http404
# from django.template import RequestContext
# from django.views.decorators.csrf import csrf_exempt
username = ""

# @csrf_exempt
def login(req):
    if req.method == 'POST':
        user_id = req.POST.get("user_id", "")
        pwd = req.POST.get("password", "")
        type_value = req.POST.get("type", "")
        if type_value == 'student':
            user = Student.objects.filter(stuId=user_id, password=pwd)
            print u'%s,%s' % (user_id, 'userId')
            print u'%s,%s' % (pwd, 'pwd')
            print u'%s,%s' % (type_value, 'type')
            if user:
                print u'%s,%s' % (user[0].name, 's')
                req.session['user_id'] = user_id
                return HttpResponseRedirect('/student/')
        elif type_value == 'teacher':
            user = Teacher.objects.filter(teaId=user_id, password=pwd)
            print 't'
            if user:
                print u'%s,%s' % (user[0].name, 't')
                req.session['user_id'] = user_id
                return HttpResponseRedirect('/teacher/teaMain.html')
        elif type_value == 'assistant':
            user = Assistant.objects.filter(astId=user_id, password=pwd)
            print 'a'
            if user:
                print u'%s,%s' % (user[0].name, 'a')
                req.session['user_id'] = user_id
                return HttpResponseRedirect('/assistant/')
        else:
            user = None
        if user:
            return HttpResponseRedirect('/assistant/')
        else:
            return HttpResponseNotFound('<h1>用户名密码错误</h1>')
    else:
        return render_to_response('login.html', {})


def student(req):
    user_id = req.session.get('user_id', 'null')
    if user_id != 'null':
        user = Student.objects.filter(stuId=user_id)
        return render_to_response('./student/stu-main.html', {"user": user[0]})
    else:
        return HttpResponseRedirect('/login/')


def redirect_url(req, type, url):
    url = './' + type + '/' + url + ".html"
    print url
    user_id = req.session.get('user_id', 'null')
    if username != 'null':
        if type == 'student':
            user = Student.objects.filter(stuId=user_id)
        elif type == 'teacher':
            user = Teacher.objects.filter(teaId=user_id)
        elif type == 'assistant':
            user = Assistant.objects.filter(astId=user_id)
        else:
            user = 0;
        return render_to_response(url, {"user": user[0]})
    else:
        return HttpResponseRedirect('/login/')


def assistant(req):
    user_id = req.session.get('user_id', 'null')
    if username != 'null':
        user = Assistant.objects.filter(astId=user_id)
        print 'get'
        return render_to_response('assistant.html', {"user": user})
    else:
        return HttpResponseRedirect('/login/')


def logout(req):
    try:
        del req.session['username']
        return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/login/')
