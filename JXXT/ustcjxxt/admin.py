from django.contrib import admin
from models import Student,Teacher,Assistant,Course
from models import SCourse,Question,Comment,TACourse,TeaHomework,StuHomework
# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Assistant)
admin.site.register(Course)
admin.site.register(SCourse)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(TACourse)
admin.site.register(TeaHomework)
admin.site.register(StuHomework)

