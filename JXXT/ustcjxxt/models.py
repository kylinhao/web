# coding=utf-8
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
    ('t', '老师'),

)


class Student(models.Model):
    stuId = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=1, choices=sexType, blank=True)
    address = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    headPic = models.ImageField(upload_to='stuPic/', blank=True)

    class Meta:
        db_table = 'db_student'
        ordering = ["stuId"]

    def __unicode__(self):
        return u'%s %s' % (self.stuId, self.name)
        # @models.permalink
        # def get_absolute_url(self):
        #     return ('item_detail',None,{'object_id':self.stuId})


class Teacher(models.Model):
    teaId = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=1,choices=sexType, blank=True)
    address = models.CharField(max_length=60, blank=True)
    email = models.EmailField()
    headPic = models.ImageField(upload_to='stuPic/', blank=True)

    class Meta:
        db_table = 'db_teacher'
        ordering = ["teaId"]

    def __unicode__(self):
        return u'%s %s' % (self.teaId, self.name)
        # @models.permalink
        # def get_absolute_url(self):
        #     return ('item_detail',None,{'object_id':self.teaId})


class Course(models.Model):
    courseId = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=60)
    beginTime = models.DateField(blank=True)
    endTime = models.DateField(blank=True)
    classTime = models.CharField(max_length=30)
    classroom = models.CharField(max_length=30)
    examTime = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'db_course'
        ordering = ["courseId"]

    def __unicode__(self):
        # return  self.courseId
        return u'%s %s' % (self.courseId, self.name)


class Assistant(models.Model):
    astId = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=30)
    beginTime = models.DateField()
    endTime = models.DateField()
    headPic = models.ImageField(upload_to='stuPic/', blank=True)

    class Meta:
        db_table = 'db_assistant'

    def __unicode__(self):
        return u'%s %s' % (self.astId, self.name)


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    stuId = models.ForeignKey(Student)
    courseId = models.ForeignKey(Course)

    class Meta:
        db_table = 'db_question'

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.stuId, self.courseId)


class Comment(models.Model):
    questionId = models.ForeignKey(Question)
    commentId = models.CharField(max_length=30)
    content = models.TextField()
    type = models.CharField(max_length=1, choices=commentatorTyep)

    class Meta:
        db_table = 'db_comment'


class TACourse(models.Model):
    teaId = models.ForeignKey(Teacher)
    astId = models.ForeignKey(Assistant, blank=True)
    courseId = models.ForeignKey(Course)

    class Meta:
        db_table = 'db_teacher_assistant_course'
        unique_together = (('teaId', 'courseId'),)

    def __unicode__(self):
        return u'%s %s' % (self.astId, self.name)


class SCourse(models.Model):
    stuId = models.ForeignKey(Student)
    courseId = models.ForeignKey(Course)
    score = models.IntegerField(blank=True)

    class Meta:
        db_table = 'db_student_course'
        unique_together = (('stuId', 'courseId'),)

    def __unicode__(self):
        return u'%s %s' % (self.stuId, self.courseId)


# 老师 布置作业
class TeaHomework(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="/homework/", blank=True)
    courseId = models.ForeignKey(Course)
    teaId = models.ForeignKey(Teacher)

    class Meta:
        db_table = 'db_teacher_homework'

    def __unicode__(self):
        return self.title


# 学生 交作业
class StuHomework(models.Model):
    score = models.IntegerField(blank=True)
    attachment = models.FileField(upload_to="/homework/", blank=True)
    stuId = models.ForeignKey(Student)
    courseId = models.ForeignKey(Course)
    teaId = models.ForeignKey(Teacher)
    astId = models.ForeignKey(Assistant, blank=True)

    class Meta:
        db_table = 'db_student_homework'

    def __unicode__(self):
        return self.stuId
