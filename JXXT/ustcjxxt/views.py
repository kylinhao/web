# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect, StreamingHttpResponse
from django import forms
from .models import *
from django.template import RequestContext
import datetime


def get_type(role_type):
    if role_type == 'student':
        return 'stu_id'
    elif role_type == 'teacher':
        return 'tea_id'
    else:
        return 'ast_id'


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
        print u'%s %s %s' % (user_id, pwd, type_value)
        if type_value == 'student':
            user = Student.objects.filter(stuId=user_id, password=pwd)
            
            if user:
                # print u'%s,%s' % (user[0].name, 's')
                req.session['user_id'] = user_id
                username = user[0].name
                print "hello"
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
        print "error"
        if not user:
            error = 1
            print error
            return render_to_response('login.html', {"error": error})
    return render_to_response('login.html', {})


def student(req):
    user_id = req.session.get('user_id', 'null')
    print 'student'
    if user_id != 'null':
        user = Student.objects.filter(stuId=user_id)
        return render_to_response('./student/homepage.html', {"user": user[0]})
    else:
        return HttpResponseRedirect('/')


def teacher(req):
    # type = get_type('teacher')
    user_id = req.session.get('user_id', 'null')
    print user_id
    if user_id != 'null':
        user = Teacher.objects.filter(teaId=user_id)
        return render_to_response('teacher/homepage.html', {"user": user[0]})
    else:
        return HttpResponseRedirect('/')


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
            user = 0
        return render_to_response(url, {"user": user[0]})
    else:
        return HttpResponseRedirect('/')


def homepage(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'homepage'
    result_type = 0
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, role_type)
    return render_to_response(role_type + '/homepage.html', {"user": user[0], "result_type": result_type})


def info(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'info'
    result_type = 0
    if user_id == 'null':
        return HttpResponseRedirect('/')
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
        return HttpResponseRedirect('/')

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


def str2num(weekday, grid):
    pos = 0
    if cmp(weekday, '周一'.decode('utf-8')) == 0:
        pos += 0
    elif cmp(weekday, '周二'.decode('utf-8')) == 0:
        pos += 5
    elif cmp(weekday, '周三'.decode('utf-8')) == 0:
        pos += 10
    elif cmp(weekday, '周四'.decode('utf-8')) == 0:
        pos += 15
    elif cmp(weekday, '周五'.decode('utf-8')) == 0:
        pos += 20

    if grid == 1:
        pos += 0
    elif grid == 3:
        pos += 1
    elif grid == 5:
        pos += 2
    elif grid == 7:
        pos += 3
    elif grid == 9:
        pos += 4

    return pos


def stu_schedule(req):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/')

    my_courses = SCourse.objects.filter(stuId=user_id)
    class_time = []
    class_name = []
    for sc in my_courses:
        course = Course.objects.filter(courseId=sc.courseId.courseId)
        if course:
            class_time.append(course[0].classTime)
            class_name.append(course[0].name)

    my_schedule = [[0 for col in range(7)] for row in range(5)]
    print my_schedule
    for i in range(len(class_time)):
        weekday = class_time[i][0:2]
        print u'%s' % weekday
        grid = class_time[i][4:5]
        pos = str2num(weekday, int(grid))
        row = pos % 5
        col = pos / 5
        my_schedule[row][col] = class_name[i]

    for arr in my_schedule:
        for item in arr:
            if item == 0:
                item = ' '

    am1 = my_schedule[0]
    am2 = my_schedule[1]
    pm1 = my_schedule[2]
    pm2 = my_schedule[3]
    night = my_schedule[4]
    user = get_user(user_id, 'student')
    return render_to_response('student/schedule.html', {"user": user[0], "am1": am1, "am2": am2,
                                                        "pm1": pm1, "pm2": pm2, "night": night})


def select_course(req):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/')

    if req.method == 'POST':
        c_id = req.POST.get("c-id", None)
        operate_type = req.POST.get("operate-type")
        print operate_type
        if operate_type == "cancel":
            SCourse.objects.filter(stuId=user_id, courseId=c_id).delete()
        else:
            user = get_user(user_id, 'student')
            c = Course.objects.get(courseId=c_id)
            new_sc = SCourse(stuId=user[0], courseId=c, score=0)
            new_sc.save()
        return HttpResponseRedirect('/student/select-course/', {})
    c_info = Course.objects.all()
    sc_list = []
    sced_list = []
    for c in c_info:
        # get teacher of each course
        tac = TACourse.objects.filter(courseId=c.courseId)
        # get the number of stu who has selected this course
        t_num = SCourse.objects.filter(courseId=c.courseId).count()

        sc = [c, tac, t_num]
        print sc
        is_selected = SCourse.objects.filter(stuId=user_id, courseId=c.courseId)
        if is_selected:
            sced_list.append(sc)
        else:
            sc_list.append(sc)
    user = get_user(user_id, 'student')
    return render_to_response('student/select-course.html',
                              {"user": user[0], "sc_list": sc_list, "sced_list": sced_list})


def stu_homework(req, line_id=0):
    user_id = req.session.get('user_id', 'null')
    print user_id
    # print line_id
    if user_id == 'null':
        return HttpResponseRedirect('/')
    # 获取当前学生所选课程c
    courses_info = SCourse.objects.filter(stuId=user_id)
    # print courses_info
    # homework list
    h_list = []
    for c in courses_info:
        homework_info = TeaHomework.objects.filter(courseId=c.courseId)
        for h in homework_info:
            h_list.append(h)
    user = get_user(user_id, 'student')
    line_id = int(line_id)
    return render_to_response('student/homework.html', {"user": user[0], "h_list": h_list, "line_id": line_id})


def stu_exam(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'stu_exam'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'student')
    exam_list = []
    c_list = Course.objects.filter(scourse__stuId=user_id)
    for c in c_list:
        sc = SCourse.objects.get(stuId=user_id,courseId=c.courseId)
        exam_list.append([c,sc.score])
    return render_to_response('student/exam.html', {"user": user[0], "exam_list": exam_list})


class UploadFileForm(forms.Form):
    file = forms.FileField()


def homework_submit(req, line_id=0):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'stu_homework_submit'
    if user_id == 'null':
        return HttpResponseRedirect('/')

    if req.method == 'POST':
        print 'post'
        form = UploadFileForm(req.POST, req.FILES)
        print u'%s' % form
        if form.is_valid():
            tea_homework_id = req.POST.get("tea-homework-id", None)
            s = StuHomework.objects.get(homeworkId=tea_homework_id)
            s.attachment = req.FILES["file"]
            s.attachment.name = req.FILES["file"].name
            s.save()
        return HttpResponseRedirect('/student/homework-submit', {})

    stu_list = StuHomework.objects.filter(stuId=user_id)

    tea_list = TeaHomework.objects.filter(stuhomework__stuId=user_id)
    st = []
    for i in range(len(stu_list)):
        s = [tea_list[i], stu_list[i]]
        st.append(s)
    # print st
    user = get_user(user_id, 'student')
    form = UploadFileForm()
    line_id = int(line_id)
    return render_to_response('student/homework-submit.html',
                              {"user": user[0], "st": st, 'form': form, 'line_id': line_id},
                              context_instance=RequestContext(req))


def stu_question(req):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'student')
    if req.method == 'POST':
        if req.POST.get("question_name", "") != "" and req.POST.get("question_information", "") != "":
            print "post"
            # print req.POST.get("course_name")
            course_name = req.POST.get("course_name")
            course_id = course_name[6:9]
            print course_id
            new_question = Question()
            now = datetime.datetime.now()
            new_question.title = req.POST.get("question_name")
            new_question.content = req.POST.get("question_information")
            new_question.stuId = user[0]
            new_question.courseId = Course.objects.filter(courseId=course_id)[0]
            new_question.time = now
            new_question.save()
        return HttpResponseRedirect('/student/question/', {})
    # get course
    c_list = SCourse.objects.filter(stuId=user_id).order_by('courseId')
    q_list = []
    for c in c_list:
        q = Question.objects.filter(courseId=c.courseId)
        if q:
            q_list.append(q)
    return render_to_response('student/question.html', {"user": user[0], "c_list": c_list, "q_list": q_list})


def stu_question_detail(req, q_id):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'stu_question_detail'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'student')

    q = Question.objects.get(id=q_id)
    print q
    if req.method == 'POST':
        reply = req.POST.get("reply", None)
        now = datetime.datetime.now()
        comment = Comment(questionId=q, commentId=user_id, content=reply, type=user_id[0], time=now)
        comment.save()
        return HttpResponseRedirect('/student/question/' + q_id, {})
    # get course

    comments = Comment.objects.filter(questionId=q_id)
    c_list = []
    for c in comments:
        if c.type == 't':
            t = Teacher.objects.get(teaId=c.commentId)
        elif c.type == 's':
            t = Student.objects.get(stuId=c.commentId)
        else:
            t = Assistant.objects.get(astId=c.commentId)
        c_list.append([c, t.name])
        #  q_id = int(q_id)
    return render_to_response('student/question-detail.html', {"user": user[0], "q": q, "c_list": c_list})


def assistant(req):
    user_id = req.session.get('user_id', 'null')
    print 'assitant'
    if user_id != 'null':
        user = Assistant.objects.filter(astId=user_id)
        print 'get'
        return render_to_response('assistant/homepage.html', {"user": user[0]})
    else:
        return HttpResponseRedirect('/')


def about_us(req, role_type):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'about-us'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, role_type)
    return render_to_response(role_type + '/about-us.html', {"user": user[0]})


def logout(req):
    try:
        del req.session['user_id']
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')


def tea_course(req, course_id=0):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/')
    c_info = Course.objects.filter(tacourse__teaId=user_id)
    print c_info
    user = get_user(user_id, 'teacher')
    if course_id == 0:
        return render_to_response('teacher/course.html', {"user": user[0], "c_info": c_info})
    else:
        if req.method == 'POST':
            print req.POST.get("course-id", "course id")
            print req.POST.get("stu-id")
            stu_id = req.POST.get("stu-id", None)
            sc_record = SCourse.objects.get(stuId=stu_id, courseId=course_id)
            sc_record.score = req.POST.get("score", None)
            sc_record.save()
            return HttpResponseRedirect('/teacher/course/' + course_id, {})
        sc_info = SCourse.objects.filter(courseId=course_id)
        c_info = Course.objects.filter(scourse__courseId=course_id)
        print sc_info
        print c_info
        sc = []
        for i in range(len(sc_info)):
            t = [c_info[i], sc_info[i]]
            sc.append(t)

        return render_to_response('teacher/grade.html', {"user": user[0], "sc": sc})


def tea_homework(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'tea_homework'
    if user_id == 'null':
        return HttpResponseRedirect('/')

    if req.method == 'POST':
        operate_type = req.POST.get("operate", None)
        h_id = req.POST.get("h-id", None)
        print operate_type, h_id
        if operate_type == u'提交':
            form = UploadFileForm(req.POST, req.FILES)
            print u'%s' % form
            if form.is_valid():
                h = TeaHomework.objects.get(id=h_id)
                h.attachment = req.FILES["file"]
                h.attachment.name = req.FILES["file"].name
                h.save()
        elif operate_type == u'删除':
            h = TeaHomework.objects.get(id=h_id)
            h.attachment.delete()
            h.save()
        return HttpResponseRedirect('/teacher/homework/', {})
    form = UploadFileForm()
    h_list = TeaHomework.objects.filter(teaId=user_id)
    user = get_user(user_id, 'teacher')
    return render_to_response('teacher/homework.html', {"user": user[0], "h_list": h_list, "form": form})


def tea_exam(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'tea_exam'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    c_list = TACourse.objects.filter(teaId=user_id)
    user = get_user(user_id, 'teacher')
    return render_to_response('teacher/exam.html', {"user": user[0], "c_list": c_list})


def tea_schedule(req):
    user_id = req.session.get('user_id', 'null')
    if user_id == 'null':
        return HttpResponseRedirect('/')

    class_time = []
    class_name = []
    course = Course.objects.filter(tacourse__teaId=user_id)
    for c in course:
        class_time.append(c.classTime)
        class_name.append(c.name)

    my_schedule = [[0 for col in range(7)] for row in range(5)]
    print my_schedule
    for i in range(len(class_time)):
        weekday = class_time[i][0:2]
        # print u'%s' % weekday
        grid = class_time[i][4:5]
        pos = str2num(weekday, int(grid))
        row = pos % 5
        col = pos / 5
        my_schedule[row][col] = class_name[i]

    for arr in my_schedule:
        for item in arr:
            if item == 0:
                item = ' '

    print 'teacher\'s schedule is ', my_schedule

    am1 = my_schedule[0]
    am2 = my_schedule[1]
    pm1 = my_schedule[2]
    pm2 = my_schedule[3]
    night = my_schedule[4]
    user = get_user(user_id, 'teacher')
    return render_to_response('teacher/schedule.html', {"user": user[0], "am1": am1, "am2": am2,
                                                        "pm1": pm1, "pm2": pm2, "night": night})


def tea_question(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    if user_id == 'null':
        return HttpResponseRedirect('/')

    user = get_user(user_id, 'teacher')
    # get course
    tac_list = TACourse.objects.filter(teaId=user_id).order_by('courseId', 'astId')
    tc_list = []  # should be assistant course list
    q_list = []
    i = 0
    length = len(tac_list)
    while i < length:
        t_list = []
        t_list.append(tac_list[i].astId)
        j = i + 1
        while j < length:
            if tac_list[j].courseId == tac_list[i].courseId:
                t_list.append(tac_list[j].astId)
                j = j + 1
            else:
                break
        tc_list.append([tac_list[i].courseId, t_list])
        i = j
    for tc in tc_list:
        print tc
        q = Question.objects.filter(courseId=tc[0])
        q_list.append(q)
    return render_to_response('teacher/question.html', {"user": user[0], "tc_list": tc_list, "q_list": q_list})


def tea_question_detail(req, q_id):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'ast_question_detail'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'teacher')

    q = Question.objects.get(id=q_id)
    print q
    if req.method == 'POST':
        reply = req.POST.get("reply", None)
        now = datetime.datetime.now()
        comment = Comment(questionId=q, commentId=user_id, content=reply, type=user_id[0], time=now)
        comment.save()
        return HttpResponseRedirect('/teacher/question/' + q_id, {})
    # get course

    comments = Comment.objects.filter(questionId=q_id)
    c_list = []
    for c in comments:
        if c.type == 't':
            t = Teacher.objects.get(teaId=c.commentId)
        elif c.type == 's':
            t = Student.objects.get(stuId=c.commentId)
        else:
            t = Assistant.objects.get(astId=c.commentId)
        c_list.append([c, t.name])
        #  q_id = int(q_id)
    return render_to_response('teacher/question-detail.html', {"user": user[0], "q": q, "c_list": c_list})


def ast_homework(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'ast_homework'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    if req.method == 'POST':
        score = req.POST.get("score", 0)
        h_id = req.POST.get("h_id", 0)
        if score and h_id:
            stu_h = StuHomework.objects.get(id=h_id)
            stu_h.score = score
            stu_h.save()
        return HttpResponseRedirect('/assistant/homework/', {})
    user = get_user(user_id, 'assistant')
    # get course
    tac_list = TACourse.objects.filter(astId=user_id).order_by('courseId', 'teaId')
    for tac in tac_list:
        print u'%s %s %s' % (tac.courseId, tac.teaId, tac.astId)

    i = 0
    length = len(tac_list)
    # teacher course list
    tc_list = []
    sh_list = []
    th_list = []
    while i < length:
        # get teacher
        t_list = []
        t_list.append(tac_list[i].teaId)
        j = i + 1
        while j < length:
            if tac_list[j].courseId == tac_list[i].courseId:
                t_list.append(tac_list[j].teaId)
                j = j + 1
            else:
                break
        tc_list.append([tac_list[i].courseId, t_list])
        th_es = TeaHomework.objects.filter(courseId=tac_list[i].courseId)
        for th in th_es:
            th_list.append([tac_list[i].courseId, th])
        i = j
    print th_list
    for th in th_list:
        sh = StuHomework.objects.get(homeworkId=th[1].id)
        sh_list.append([th[0], sh])

    return render_to_response('assistant/homework.html', {"user": user[0], "tc_list": tc_list, "sh_list": sh_list})


def ast_question(req):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'ast_question'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'assistant')
    # get course
    tac_list = TACourse.objects.filter(astId=user_id).order_by('courseId', 'teaId')
    tc_list = []
    q_list = []
    i = 0
    length = len(tac_list)
    # teacher course list
    while i < length:
        # get teacher
        t_list = []
        t_list.append(tac_list[i].teaId)
        j = i + 1
        while j < length:
            if tac_list[j].courseId == tac_list[i].courseId:
                t_list.append(tac_list[j].teaId)
                j = j + 1
            else:
                break
        tc_list.append([tac_list[i].courseId, t_list])
        i = j
    for tc in tc_list:
        print tc
        q = Question.objects.filter(courseId=tc[0])
        q_list.append(q)
    return render_to_response('assistant/question.html', {"user": user[0], "tc_list": tc_list, "q_list": q_list})


def ast_question_detail(req, q_id):
    user_id = req.session.get('user_id', 'null')
    print user_id
    print 'ast_question_detail'
    if user_id == 'null':
        return HttpResponseRedirect('/')
    user = get_user(user_id, 'assistant')

    q = Question.objects.get(id=q_id)
    print q
    if req.method == 'POST':
        reply = req.POST.get("reply", None)
        now = datetime.datetime.now()
        comment = Comment(questionId=q, commentId=user_id, content=reply, type=user_id[0], time=now)
        comment.save()
        return HttpResponseRedirect('/assistant/question/' + q_id, {})
    # get course

    comments = Comment.objects.filter(questionId=q_id)
    c_list = []
    for c in comments:
        if c.type == 't':
            t = Teacher.objects.get(teaId=c.commentId)
        elif c.type == 's':
            t = Student.objects.get(stuId=c.commentId)
        else:
            t = Assistant.objects.get(astId=c.commentId)
        c_list.append([c, t.name])
        #  q_id = int(q_id)
    return render_to_response('assistant/question-detail.html', {"user": user[0], "q": q, "c_list": c_list})


def download(request, homework_role, filename):
    filename = 'upload/' + homework_role + '/' + filename

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)

    return response
