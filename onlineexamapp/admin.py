from django.contrib import admin
from onlineexamapp.models import (Exam,Center,Subject,Exam_Subject_Bridge,Question_Master,Question_Exam_Bridge,
Question_Option,Questions_Answer_bridge,Student,Answer_Sheet,Student_Exam_Flag)

admin.site.register(Exam)
admin.site.register(Center)
admin.site.register(Subject)
admin.site.register(Exam_Subject_Bridge)
admin.site.register(Question_Option)
#admin.site.register(Question_Master)
admin.site.register(Question_Exam_Bridge)
admin.site.register(Questions_Answer_bridge)
admin.site.register(Student)
admin.site.register(Answer_Sheet)
admin.site.register(Student_Exam_Flag)

@admin.register(Question_Master)
class Question_MasterAdmin(admin.ModelAdmin):
    list_display=("question","question_difficulty_level")

# Register your models here.
