from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'JXXT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'ustcjxxt.views.login'),
    url(r'^student/$', 'ustcjxxt.views.student'),
    url(r'^teacher/$', 'ustcjxxt.views.teacher'),
    # url(r'^(.+)/(.+)/$','ustcjxxt.views.redirect_url'),
    url(r'^(.+)/info/$', 'ustcjxxt.views.info'),
    url(r'^(.+)/change-password/$', 'ustcjxxt.views.change_pwd'),
    url(r'^(.+)/homepage/$', 'ustcjxxt.views.homepage'),
    url(r'^student/homework/$', 'ustcjxxt.views.stu_homework'),
    url(r'^student/homework/(\d+)/$', 'ustcjxxt.views.stu_homework', name='stu_homework'),
    url(r'^student/select-course/$', 'ustcjxxt.views.select_course'),
    url(r'^student/schedule/$', 'ustcjxxt.views.stu_schedule'),
    url(r'^student/exam/$', 'ustcjxxt.views.stu_exam'),
    url(r'^student/homework-submit/$', 'ustcjxxt.views.homework_submit'),
    url(r'^student/homework-submit/(\d+)/$', 'ustcjxxt.views.homework_submit', name='homework_submit'),
    url(r'^student/question/$', 'ustcjxxt.views.stu_question'),
    url(r'^student/question/(\d+)$', 'ustcjxxt.views.stu_question_detail', name='stu_question_detail'),

    url(r'^teacher/course/$', 'ustcjxxt.views.tea_course'),
    url(r'^teacher/course/(.+)/$', 'ustcjxxt.views.tea_course', name='upload_score'),
    url(r'^teacher/homework/$', 'ustcjxxt.views.tea_homework'),
    url(r'^teacher/exam/$', 'ustcjxxt.views.tea_exam'),
    url(r'^teacher/schedule/$', 'ustcjxxt.views.tea_schedule'),
    url(r'^teacher/question/$', 'ustcjxxt.views.tea_question'),
    url(r'^teacher/question/(\d+)$', 'ustcjxxt.views.tea_question_detail', name='tea_question_detail'),


    url(r'^assistant/$', 'ustcjxxt.views.assistant'),
    url(r'^assistant/homework/$', 'ustcjxxt.views.ast_homework'),
    url(r'^assistant/question/$', 'ustcjxxt.views.ast_question'),
    url(r'^assistant/question/(\d+)$', 'ustcjxxt.views.ast_question_detail', name='ast_question_detail'),

    url(r'^upload/(.+)/(.+)$', 'ustcjxxt.views.download'),

    url(r"^logout/$", 'ustcjxxt.views.logout'),
    url(r'^(.+)/about-us/$', 'ustcjxxt.views.about_us'),
]
