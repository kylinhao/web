# coding=utf-8
from django.db import models

# Create your models here.
#  python manage.py validate ,if there might be something wrong in your the model
#  python manage.py sqlall books, books the name of your app
sexType = (
    ('m', '男'),
    ('f', '女')
)


class Student(models.Model):
    studentId = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=1, choices=sexType)
    address = models.CharField(max_length=60,blank=True)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='stuPic/',blank=True)

    class Meta:
        ordering = ["studentId"]

    def __unicode__(self):
        return self.studentId
        # @models.permalink
        # def get_absolute_url(self):
        #     return ('item_detail',None,{'object_id':self.studentId})


class Teacher(models.Model):
    teacherId = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=1, choices=sexType)
    address = models.CharField(max_length=60,blank=True)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='stuPic/',blank=True)

    class Meta:
        ordering = ["teacherId"]

    def __unicode__(self):
        return self.teacherId
        # @models.permalink
        # def get_absolute_url(self):
        #     return ('item_detail',None,{'object_id':self.teacherId})


class Assistant(models.Model):
    astId = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=60)
    teacher = models.ManyToManyField(Teacher)
    beginTime = models.DateField()
    endTime = models.DateField()
    assitant = models.ForeignKey(Student)
    comment = models.TextField(max_length=500)
    def __unicode__(self):
        return self.astId
