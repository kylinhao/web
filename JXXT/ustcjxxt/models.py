# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#  python manage.py validate ,if there might be something wrong in your the model
#  python manage.py sqlall books, books the name of your app
sexType = (
    ('m', '男'),
    ('f', '女')
)
commentatorTyep = (
    ('s', '学生'),
    ('a', '助教'),
    ('t', '教师'),

)


class Student(models.Model):
    stuId = models.CharField(u'学号', max_length=20, primary_key=True)
    password = models.CharField(u'密码', max_length=60)
    name = models.CharField(u'姓名', max_length=30)
    age = models.IntegerField(u'年龄', blank=True)
    sex = models.CharField(u'性别', max_length=1, choices=sexType, blank=True)
    address = models.CharField(u'地址', max_length=60, blank=True)
    email = models.EmailField(u'邮箱', blank=True)
    headPic = models.ImageField(u'头像', upload_to='stuPic/', blank=True)

    class Meta:
        db_table = 'db_student'
        # verbose_name =u'学生'
        verbose_name_plural = u'学生'
        ordering = ["stuId"]

    def __unicode__(self):
        return u'%s %s' % (self.stuId, self.name)


class Teacher(models.Model):
    teaId = models.CharField(u'工号', max_length=20, primary_key=True)
    password = models.CharField(u'密码', max_length=60)
    name = models.CharField(u'姓名', max_length=30)
    age = models.IntegerField(u'年龄', blank=True)
    sex = models.CharField(u'性别', max_length=1, choices=sexType, blank=True)
    address = models.CharField(u'地址', max_length=60, blank=True)
    email = models.EmailField(u'邮箱', blank=True)
    headPic = models.ImageField(u'头像', upload_to='teaPic/', blank=True)

    class Meta:
        db_table = 'db_teacher'
        ordering = ["teaId"]
        verbose_name_plural = u'教师'

    def __unicode__(self):
        return u'%s %s' % (self.teaId, self.name)


class Assistant(models.Model):
    astId = models.CharField(u'工号', max_length=30, primary_key=True)
    password = models.CharField(u'密码', max_length=60)
    name = models.CharField(u'姓名', max_length=30)
    age = models.IntegerField(u'年龄', blank=True)
    sex = models.CharField(u'性别', max_length=1, choices=sexType, blank=True)
    address = models.CharField(u'地址', max_length=60, blank=True)
    email = models.EmailField(u'邮箱', blank=True)
    headPic = models.ImageField(u'头像', upload_to='teaPic/', blank=True)
    beginTime = models.DateField(u'开始时间')
    endTime = models.DateField(u'结束时间')

    class Meta:
        db_table = 'db_assistant'
        verbose_name_plural = u'助教'

    def __unicode__(self):
        return u'%s %s' % (self.astId, self.name)


class Course(models.Model):
    courseId = models.CharField(u'课程号', max_length=30, primary_key=True)
    name = models.CharField(u'姓名', max_length=60)
    beginTime = models.DateField(u'开始时间', blank=True)
    endTime = models.DateField(u'结束时间', blank=True)
    classTime = models.CharField(u'上课时间', max_length=30)
    classroom = models.CharField(u'教室', max_length=30)
    examTime = models.CharField(u'考试时间', max_length=100, blank=True)
    ps = models.TextField(u'备注')

    class Meta:
        db_table = 'db_course'
        ordering = ["courseId"]
        verbose_name_plural = u'课程'

    def __unicode__(self):
        # return  self.courseId
        return u'%s %s' % (self.courseId, self.name)


class SCourse(models.Model):
    stuId = models.ForeignKey(Student, verbose_name=u'学生学号')
    courseId = models.ForeignKey(Course, verbose_name=u'课程号')
    score = models.IntegerField('成绩', blank=True)

    class Meta:
        db_table = 'db_student_course'
        unique_together = (('stuId', 'courseId'),)
        verbose_name_plural = u'选课'

    def __unicode__(self):
        return u'%s %s' % (self.stuId, self.courseId)


class Question(models.Model):
    title = models.CharField('问题', max_length=100)
    content = models.TextField('详情', blank=True)
    stuId = models.ForeignKey(Student, verbose_name=u'学生学号')
    courseId = models.ForeignKey(Course, verbose_name=u'课程号')
    time = models.DateTimeField(u'时间')

    class Meta:
        db_table = 'db_question'
        verbose_name_plural = u'问题'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)


class Comment(models.Model):
    questionId = models.ForeignKey(Question, verbose_name=u'问题Id')
    commentId = models.CharField(u'评论者Id', max_length=30)
    content = models.TextField(u'内容')
    type = models.CharField(u'角色', max_length=1, choices=commentatorTyep)
    time = models.DateTimeField(u'时间')

    class Meta:
        db_table = 'db_comment'
        verbose_name_plural = u'评论'

    def __unicode__(self):
        return u'%s' % self.content


class TACourse(models.Model):
    teaId = models.ForeignKey(Teacher, verbose_name=u'教师工号')
    astId = models.ForeignKey(Assistant, verbose_name=u'助教工号', blank=True)
    courseId = models.ForeignKey(Course, verbose_name=u'课程号')

    class Meta:
        db_table = 'db_teacher_assistant_course'
        unique_together = (('teaId', 'courseId'),)
        verbose_name_plural = u'教师-助教-课程'

    def __unicode__(self):
        return u'%s' % self.astId


# 教师 布置作业
class TeaHomework(models.Model):
    title = models.CharField(u'作业', max_length=100)
    content = models.TextField(u'内容', blank=True)
    attachment = models.FileField(u'附件', upload_to="teaHomework/", blank=True)
    courseId = models.ForeignKey(Course, verbose_name=u'课程号')
    teaId = models.ForeignKey(Teacher, verbose_name=u'教师工号')

    class Meta:
        db_table = 'db_teacher_homework'
        verbose_name_plural = u'布置作业'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)


# 学生 交作业
class StuHomework(models.Model):
    score = models.IntegerField(u'成绩', blank=True)
    attachment = models.FileField(u'附件', upload_to="stuHomework/", blank=True)
    stuId = models.ForeignKey(Student, verbose_name=u'学生学号')
    homeworkId = models.OneToOneField(TeaHomework, verbose_name=u'作业')

    class Meta:
        db_table = 'db_student_homework'
        verbose_name_plural = u'提交作业'

    def __unicode__(self):
        return u'%s %s' % (self.stuId, self.homeworkId)
