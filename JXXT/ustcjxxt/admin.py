from django.contrib import admin
from models import Student, Teacher, Assistant, Course
from models import SCourse, Question, Comment, TACourse, TeaHomework, StuHomework
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'name', 'age', 'sex', 'address', 'email')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teaId', 'name', 'age', 'sex', 'address', 'email')


class AssistantAdmin(admin.ModelAdmin):
    list_display = ('astId', 'name', 'beginTime', 'endTime')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseId', 'name', 'beginTime', 'endTime', 'classTime', 'classroom', 'examTime')


class SCourseAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'courseId', 'score')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'stuId', 'courseId')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('questionId', 'commentId', 'content', 'type')


class TACourseAdmin(admin.ModelAdmin):
    list_display = ('teaId', 'astId', 'courseId')


class TeaHomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'attachment', 'courseId', 'teaId')


class StuHomeworkAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'score', 'attachment', 'homeworkId')


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(SCourse, SCourseAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(TACourse,TACourseAdmin)
admin.site.register(TeaHomework,TeaHomeworkAdmin)
admin.site.register(StuHomework, StuHomeworkAdmin)
