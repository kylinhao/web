# coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from .models import Student, Teacher, Assistant, SCourse, TeaHomework, Course, Question
# from django.http import Http404
# from django.template import RequestContext
# from django.views.decorators.csrf import csrf_exempt
global username
username = ""


def get_user(user_id, role_type):
    if role_type == 'student':
        user = Student.objects.filter(stuId=user_id)
    elif role_type == 'teacher':
        user = Teacher.objects.filter(teaId=user_id)
    elif role_type == 'assistant':
        user = Assistant.objects.filter(astId=user_id)
    else:
        user = 0
    return user


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
                username = user[0].name
                return HttpResponseRedirect('/student/')
        elif type_value == 'teacher':
            user = Teacher.objects.filter(teaId=user_id, password=pwd)
            print 't'
            if user:
                print u'%s,%s' % (user[0].name, 't')
                req.session['user_id'] = user_id
                return HttpResponseRedirect('/teacher/')
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
    if user_id != 'null':
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


def homepage(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'homepage'
    result_type = 0
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    user = get_user(user_id, role_type)
    return render_to_response(role_type + '/homepage.html', {"user": user[0], "result_type": result_type})


def info(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'info'
    result_type = 0
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    user = get_user(user_id, role_type)
    if req.method == 'POST':
        print 'post'
        addr = req.POST.get("address", "")
        mail = req.POST.get("email", "")
        user.update(address=addr, email=mail)
        result_type = 1
    print result_type
    user = get_user(user_id, role_type)
    return render_to_response(role_type + '/info.html', {"user": user[0], "result_type": result_type})


def change_pwd(req, role_type):
    print role_type
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/login/')

    result_type = 0
    user = get_user(user_id, role_type)
    if req.method == 'POST':
        old_pwd = req.POST.get("old_pwd")
        new_pwd = req.POST.get("new_pwd")
        confirm_pwd = req.POST.get("confirm_pwd")
        print old_pwd, new_pwd, confirm_pwd
        if user[0].password == old_pwd and new_pwd == confirm_pwd:
            # user[0].password = new_pwd
            user.update(password=new_pwd)
            result_type = 1
        else:
            result_type = 2
    print result_type
    return render_to_response(role_type + '/change-password.html', {"user": user[0], "result_type": result_type})


def homework(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'info'
    result_type = 0
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    # 获取当前学生所选课程c
    courses_info = SCourse.objects.filter(stuId=user_id)
    print courses_info
    # 获取对应课程的name
    homework_list = []
    for c in courses_info:
        homework_info = TeaHomework.objects.filter(courseId=c.courseId)
        for h in homework_info:
            homework_list.append(h)
    user = get_user(user_id, role_type)
    return render_to_response(role_type + '/homework.html', {"user": user[0], "homework_list": homework_list})


def stu_exam(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'stu_exam'
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    user = get_user(user_id, 'student')
    exam_time = Course.objects.filter(scourse__stuId =user_id);
    return render_to_response('student/exam.html', {"user": user[0], "exam_time": exam_time})

def homework_submit(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'stu_exam'
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    user = get_user(user_id, 'student')
    exam_time =[]
    return  render_to_response('student/homework-submit.html', {"user": user[0], "exam_time": exam_time})

def assistant(req):
    user_id = req.session.get('user_id', 'null')
    if user_id != 'null':
        user = Assistant.objects.filter(astId=user_id)
        print 'get'
        return render_to_response('assistant.html', {"user": user})
    else:
        return HttpResponseRedirect('/login/')


def logout(req):
    try:
        del req.session['user_id']
        return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/login/')


def get_courseId_by_name(course_name):
    course = Course.objects.filter(name=course_name)
    return course[0]


def submit_questions(req, role_type):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/login/')
    print role_type
    user = get_user(user_id, role_type)
    if req.method == 'POST':
        if req.POST.get("question_name", "") != "" and req.POST.get("question_information", "") != "":
            print "post"
            # print req.POST.get("course_name")
            course_name = req.POST.get("course_name")
            new_question = Question()
            new_question.title = req.POST.get("question_name")
            new_question.content = req.POST.get("question_information")
            new_question.stuId = user[0]
            new_question.courseId = get_courseId_by_name(course_name)
            new_question.save()

    elif req.method == 'GET':
        print "get"
    course_list = []
    question_list = []
    course_student = SCourse.objects.filter(stuId=user_id)
    for cs in course_student:
        course = Course.objects.filter(courseId=cs.courseId.courseId)
        course_list.append(course[0].name)
        question = Question.objects.filter(courseId=cs.courseId.courseId)
        for q in question:
            question_list.append(q)
    return render_to_response('student/question.html', {"courses_name": course_list, "question": question_list})


def get_teacher_by_teacherId(teacherId):
    teacher = Teacher.objects.filter(teaId=teacherId)
    return teacher[0]


def get_course_by_courseId(course_Id):
    course = Course.objects.filter(courseId=course_Id)
    return course[0]
